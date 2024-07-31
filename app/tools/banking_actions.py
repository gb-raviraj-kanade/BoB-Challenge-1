# from datetime import datetime
import pandas as pd

from app.config import Config
from app.config import TransactionDataColumns as TDC

def check_balance(user_name: str) -> str:
    """A function to check the recent balance of User"""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    temp_df = temp_df.sort_values(by=[TDC.TRANSACTION_DATE, TDC.TRANSACTION_TIME], ascending=False)
    balance = temp_df.iloc[0][TDC.BALANCE]
    return str(balance)

def get_transaction_history(user_name: str, dates: list[str]) -> str:
    """A function to get transaction history of User for given dates of Format (dd-mm-yyyy)"""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    dates = pd.to_datetime(dates, format="%d-%m-%Y")
    temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE].isin(dates)]
    return temp_df.to_string(index=False)

def get_full_transaction_history(user_name: str, date_start: str | None = None, date_end: str | None = None) -> str:
    """A function to get full transaction history of User or from given date_start to given date_end of Format (dd-mm-yyyy)"""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    if date_start is not None:
        date_start = pd.to_datetime(date_start, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] >= date_start]
    if date_end is not None:
        date_end = pd.to_datetime(date_end, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] <= date_end]
    temp_df = temp_df.sort_values(by=[TDC.TRANSACTION_DATE, "Transaction Time"], ascending=True)
    return temp_df.to_string(index=False)

def get_user_stats(user_name: str) -> str:
    """A function to get stats of User such as Account Number, Account Type, Customer Address, Branch Name, IFSC Code, MICR Code, Branch Address"""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    record = temp_df.iloc[0]
    return (f"Account Number: {record[TDC.ACCOUNT_NUMBER]}, "
            f"Account Type: {record[TDC.ACCOUNT_TYPE]}, "
            f"Customer Address: {record[TDC.CUSTOMER_ADDRESS]}, "
            f"Branch Name: {record[TDC.BRANCH_NAME]}, "
            f"IFSC Code: {record[TDC.IFSC_CODE]}, "
            f"MICR Code: {record[TDC.MICR_CODE]}, "
            f"Branch Address: {record[TDC.BRANCH_ADDRESS]}")

def get_total_deposits(user_name: str, date_start: str | None = None, date_end: str | None = None) -> str:
    """A function to get total deposits of User from given start date to given end date of Format (dd-mm-yyyy).
    If start and end dates are not given, it will return total deposits of User till date."""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    if date_start is not None:
        date_start = pd.to_datetime(date_start, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] >= date_start]
    if date_end is not None:
        date_end = pd.to_datetime(date_end, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] <= date_end]
    total_deposits = temp_df[temp_df[TDC.CREDIT] > 0][TDC.CREDIT].sum()
    return str(total_deposits)

def get_total_withdrawals(user_name: str, date_start: str | None = None, date_end: str | None = None) -> str:
    """A function to get total withdrawals of User from given start date to given end date of Format (dd-mm-yyyy).
    If start and end dates are not given, it will return total withdrawals of User till date."""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    if date_start is not None:
        date_start = pd.to_datetime(date_start, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] >= date_start]
    if date_end is not None:
        date_end = pd.to_datetime(date_end, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] <= date_end]
    total_withdrawals = temp_df[temp_df[TDC.DEBIT] > 0][TDC.DEBIT].sum()
    return str(total_withdrawals)

def get_largest_transaction(user_name: str, date_start: str | None = None, date_end: str | None = None) -> str:
    """A function to get largest transaction of User from given start date to given end date of Format (dd-mm-yyyy).
    If start and end dates are not given, it will return largest transaction of User till date."""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    if date_start is not None:
        date_start = pd.to_datetime(date_start, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] >= date_start]
    if date_end is not None:
        date_end = pd.to_datetime(date_end, format="%d-%m-%Y")
        temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] <= date_end]
    largest_transaction = temp_df[temp_df[TDC.DEBIT] > 0][TDC.DEBIT].max()
    largest_transaction_records = temp_df[temp_df[TDC.DEBIT] == largest_transaction]
    return largest_transaction_records.to_string(index=False)

def get_recent_transactions(user_name: str) -> str:
    """A function to get recent transactions of User"""
    transactions_df = pd.read_csv(Config.TransactionsData)
    transactions_df[TDC.TRANSACTION_DATE] = pd.to_datetime(transactions_df[TDC.TRANSACTION_DATE], format="%d-%m-%Y")
    temp_df = transactions_df[transactions_df[TDC.CUSTOMER_NAME] == user_name]
    temp_df = temp_df.sort_values(by=[TDC.TRANSACTION_DATE, TDC.TRANSACTION_TIME], ascending=False)
    last_trans_date = temp_df.iloc[0][TDC.TRANSACTION_DATE]
    temp_df = temp_df[temp_df[TDC.TRANSACTION_DATE] == last_trans_date]
    temp_df = temp_df.sort_values(by=[TDC.TRANSACTION_TIME])
    return temp_df.to_string(index=False)

# def pay_bills(user_name: str, amount: float, description: str) -> str:
#     """A function to pay bills"""
#     # TODO: Add logic to pay bills
#     return f"Successfully paid bill of Rs. {amount} for {description}"

# def report_lost_card(user_name: str) -> str:
#     """A function to report lost card"""
#     # TODO: Add logic to report lost card
#     return "Successfully reported lost card"

# def transfer_money(user_name: str, amount: float, 
#                    description: str, receiver_name: str) -> str:
#     """A function to transfer money to another user"""
#     # TODO: Add logic to transfer money
#     return f"Successfully transferred Rs. {amount} to {receiver_name}"

# def schedule_payment(user_name: str, amount: float, 
#                       description: str, date: str) -> str:
#     """A function to schedule payment"""
#     # TODO: Add logic to schedule payment
#     # Check if date is valid
#     try:
#         datetime.strptime(date, "%Y-%m-%d")
#     except ValueError:
#         return "Invalid date format. Please enter a valid date in the format YYYY-MM-DD."
#     # Check if date is in the future
#     if datetime.strptime(date, "%Y-%m-%d") < datetime.now():
#         return "Invalid date. Please enter a date in the future."
#     return f"Successfully scheduled payment of Rs. {amount} for {description} on {date}"