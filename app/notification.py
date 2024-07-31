import json
from openai import AzureOpenAI
from llama_index.core import PromptTemplate

from app.config import Config
from app.prompts.email import SYSTEM_PROMPT as EMAIL_SYSTEM_PROMPT, USER_PROMPT as EMAIL_USER_PROMPT
from app.prompts.anomaly import SYSTEM_PROMPT as ANOMALY_SYSTEM_PROMPT, USER_PROMPT as ANOMALY_USER_PROMPT
from app.tools.banking_actions import get_full_transaction_history, get_total_deposits, get_total_withdrawals, get_largest_transaction, get_recent_transactions
from dotenv import load_dotenv
load_dotenv()

class NotificationGenerator:
    def __init__(self):
        # self._llm = OpenAI()
        self._llm = AzureOpenAI()
    
    def generate_email(self, user_name: str) -> str:
        transactions_history = get_full_transaction_history(user_name, Config.PrevMonthDateStart, Config.PrevMonthDateEnd)
        deposits = get_total_deposits(user_name, Config.PrevMonthDateStart, Config.PrevMonthDateEnd)
        withdrawals = get_total_withdrawals(user_name, Config.PrevMonthDateStart, Config.PrevMonthDateEnd)
        largest_transaction = get_largest_transaction(user_name, Config.PrevMonthDateStart, Config.PrevMonthDateEnd)
        with open(f"{Config.UserInsights}/{user_name}.json", "r") as f:
            insights = json.load(f)
        user_prompt = PromptTemplate(EMAIL_USER_PROMPT).format(
            TRANSACTIONS_HISTORY=transactions_history,
            TOTAL_DEPOSITS=deposits,
            TOTAL_WITHDRAWALS=withdrawals,
            LARGEST_TRANSACTION=largest_transaction,
            INSIGHTS=insights)
        result = self._llm.chat.completions.create(
            messages=[{"role": "system", "content": EMAIL_SYSTEM_PROMPT},
                      {"role": "user", "content": user_prompt}],
            model=Config.LLMModel,
            temperature=Config.LLMModelTemperature
        ).choices[0].message.content
        result = result.replace("\n", "")
        return result
    
    def check_anomaly(self, user_name: str) -> dict:
        transaction_history = get_full_transaction_history(user_name)
        recent_trnsactions = get_recent_transactions(user_name)
        user_prompt = PromptTemplate(ANOMALY_USER_PROMPT).format(
            TRANSACTIONS_HISTORY=transaction_history,
            RECENT_TRANSACTIONS=recent_trnsactions
        )
        result = self._llm.chat.completions.create(
            messages=[{"role": "system", "content": ANOMALY_SYSTEM_PROMPT},
                      {"role": "user", "content": user_prompt}],
            model=Config.LLMModel,
            temperature=Config.LLMModelTemperature,
            response_format={"type": "json_object"}
        ).choices[0].message.content
        result = json.loads(result, strict=False)
        return result