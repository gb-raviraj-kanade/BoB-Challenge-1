import enum


class Config:
    GPT35: str = "gpt-35-turbo"
    GPT4o: str = "gpt-4o"
    
    LLMModel: str = GPT4o
    LLMModelTemperature: float = 0.0
    
    EmbeddingModel: str = "Alibaba-NLP/gte-base-en-v1.5"
    EmbedBatchSize: int = 8

    FAQDataDir: str = "data/BOB_FAQs"
    IndexDir: str = "index"
    ConversationHistory: str = "data/user_chat_history"
    UserInsights: str = "data/user_insights"
    TransactionsData: str = "data/transactions.csv"

    SimilarityTopK: int = 5
    
    GreetingMessage: str = "Hello {CustomerName}, I am BoB AI Assist, a virtual assistant from Bank of Baroda. How can I help you today?"

    PrevMonthDateStart: str = "01-07-2024"
    PrevMonthDateEnd: str = "31-07-2024"

    AzureRegion: str = "centralindia"

    SilenceThreshold = -40  # Silence threshold in dB
    MinSilenceLength = 1500   # Minimum length of silence in milliseconds

class TransactionDataColumns(str, enum.Enum):
    CUSTOMER_NAME = "Customer Name"
    ACCOUNT_NUMBER = "Account Number"
    ACCOUNT_TYPE = "Account Type"
    CUSTOMER_ADDRESS = "Customer Address"
    BRANCH_NAME = "Branch Name"
    IFSC_CODE = "IFSC Code"
    MICR_CODE = "MICR Code"
    BRANCH_ADDRESS = "Branch Address"
    TRANSACTION_DATE = "Transaction Date"
    TRANSACTION_TIME = "Transaction Time"
    DESCRIPTION = "Description"
    DEBIT = "Debit"
    CREDIT = "Credit"
    BALANCE = "Balance"

class AzureLanguages(str, enum.Enum):
    English = "en-US"
    Hindi = "hi-IN"
    Bengali = "bn-IN"
    Gujarati = "gu-IN"
    Kannada = "kn-IN"
    Malayalam = "ml-IN"
    Marathi = "mr-IN"
    Punjabi = "pa-IN"
    Tamil = "ta-IN"
    Telugu = "te-IN"
    Urdu = "ur-IN"