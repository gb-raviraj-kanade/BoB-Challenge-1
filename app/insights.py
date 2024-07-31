import json
import os

from openai import AzureOpenAI
from llama_index.core import PromptTemplate

from app.config import Config
from app.prompts.insight import SYSTEM_PROMPT, USER_PROMPT
from app.tools.banking_actions import get_full_transaction_history
from dotenv import load_dotenv
load_dotenv()

if not os.path.exists(Config.UserInsights):
    os.makedirs(Config.UserInsights)

class InsightAgent:
    def __init__(self):
        # self._llm = OpenAI()
        self._llm = AzureOpenAI()

    def get_insights(self, user_name: str) -> dict:
        if os.path.exists(f"{Config.ConversationHistory}/{user_name}.json"):
            with open(f"{Config.ConversationHistory}/{user_name}.json", "r") as f:
                conversation_history = json.load(f)
        else:
            conversation_history = {}
        transactions_history = get_full_transaction_history(user_name)
        user_prompt = PromptTemplate(USER_PROMPT).format(CONVERSATION_HISTORY=json.dumps(conversation_history, indent=2),
                                                         TRANSACTIONS_HISTORY=transactions_history)
        result = self._llm.chat.completions.create(
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                     {"role": "user", "content": user_prompt}],
            model=Config.LLMModel,
            temperature=Config.LLMModelTemperature,
            response_format={"type": "json_object"}
        ).choices[0].message.content
        result_json = json.loads(result, strict=False)
        with open(f"{Config.UserInsights}/{user_name}.json", "w") as f:
            json.dump(result_json, f, indent=2)
        
        return result_json