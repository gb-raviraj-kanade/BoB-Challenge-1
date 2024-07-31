from llama_index.core.tools import FunctionTool

from app.tools.faq_rag import faq_rag
from app.tools.banking_actions import (
    check_balance,
    get_transaction_history,
    get_full_transaction_history,
    get_user_stats,
    # report_lost_card,
    # pay_bills,
    # transfer_money,
    # schedule_payment
)

faq_tool = FunctionTool.from_defaults(fn=faq_rag)
check_balance_tool = FunctionTool.from_defaults(fn=check_balance)
get_transaction_history_tool = FunctionTool.from_defaults(fn=get_transaction_history)
get_full_transaction_history_tool = FunctionTool.from_defaults(fn=get_full_transaction_history)
get_user_stats_tool = FunctionTool.from_defaults(fn=get_user_stats)
# pay_bills_tool = FunctionTool.from_defaults(fn=pay_bills)
# report_lost_card_tool = FunctionTool.from_defaults(fn=report_lost_card)
# transfer_money_tool = FunctionTool.from_defaults(fn=transfer_money)
# schedule_payment_tool = FunctionTool.from_defaults(fn=schedule_payment)

tools = [
    faq_tool,
    check_balance_tool,
    get_transaction_history_tool,
    get_full_transaction_history_tool,
    get_user_stats_tool,
    # pay_bills_tool,
    # report_lost_card_tool,
    # transfer_money_tool,
    # schedule_payment_tool
]