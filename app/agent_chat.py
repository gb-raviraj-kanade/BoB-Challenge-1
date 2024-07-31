from datetime import datetime
import json
import os

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core import PromptTemplate
from openai.types.chat import ChatCompletionMessageToolCall

from app.config import Config
from app.prompts.agent_chat import AGENT_SYSTEM_PROMPT
from app.prompts.summarize_chat import SUMMARIZE_PROMPT
from app.tools.tools import tools
from dotenv import load_dotenv
load_dotenv()

class Agent:
    def __init__(self,
                 user_name: str,
                ) -> None:
        self._user_name = user_name
        # self._llm = OpenAI(model=Config.LLMModel, temperature=Config.LLMModelTemperature)
        self._llm = AzureOpenAI(model=Config.LLMModel, 
                                deployment_name=Config.LLMModel, 
                                temperature=Config.LLMModelTemperature,
                                api_key=os.getenv("AZURE_OPENAI_API_KEY"),
                                azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
                                api_version=os.getenv("OPENAI_API_VERSION"))
        self._tools = {tool.metadata.name: tool for tool in tools}
        if not os.path.exists(f"{Config.ConversationHistory}/{user_name}.json"):
            with open(f"{Config.ConversationHistory}/{user_name}.json", "w") as f:
                json.dump({}, f, indent=2)
        with open(f"{Config.ConversationHistory}/{user_name}.json", "r") as f:
            conversations = json.load(f)
        prompt = PromptTemplate(AGENT_SYSTEM_PROMPT).format(USER_NAME=user_name, 
                                                            CONVERSATION_HISTORY=json.dumps(conversations, indent=2))
        chat_history = [ChatMessage(role="system", content=prompt)]
        self._chat_history = chat_history

    def summarize(self) -> None:
        summarize_prompt = PromptTemplate(SUMMARIZE_PROMPT).format(USER_NAME=self._user_name)
        self._chat_history.append(ChatMessage(role="user", content=summarize_prompt))
        ai_message = self._llm.chat(self._chat_history).message
        self._chat_history.pop()
        with open(f"{Config.ConversationHistory}/{self._user_name}.json", "r") as f:
            conversations = json.load(f)
        current_datetime = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        with open(f"{Config.ConversationHistory}/{self._user_name}.json", "w") as f:
            conversations[current_datetime] = ai_message.content
            json.dump(conversations, f, indent=2)

    def chat(self, message: str) -> str:
        chat_history = self._chat_history
        chat_history.append(ChatMessage(role="user", content=message))
        tools = [
            tool.metadata.to_openai_tool() for _, tool in self._tools.items()
        ]

        ai_message = self._llm.chat(chat_history, tools=tools).message
        additional_kwargs = ai_message.additional_kwargs
        chat_history.append(ai_message)

        tool_calls = additional_kwargs.get("tool_calls", None)
        # parallel function calling is now supported
        if tool_calls is not None:
            for tool_call in tool_calls:
                function_message = self._call_function(tool_call)
                chat_history.append(function_message)
                ai_message = self._llm.chat(chat_history).message
                chat_history.append(ai_message)

        return ai_message.content

    def _call_function(
        self, tool_call: ChatCompletionMessageToolCall
    ) -> ChatMessage:
        id_ = tool_call.id
        function_call = tool_call.function
        tool = self._tools[function_call.name]
        output = tool(**json.loads(function_call.arguments))
        return ChatMessage(
            name=function_call.name,
            content=str(output),
            role="tool",
            additional_kwargs={
                "tool_call_id": id_,
                "name": function_call.name,
            },
        )