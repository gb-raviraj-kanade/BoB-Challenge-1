import os
from llama_index.core import (
    StorageContext,
    load_index_from_storage
)
# from llama_index.llms.openai import OpenAI
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from dotenv import load_dotenv

from app.config import Config

load_dotenv()

embed_model = HuggingFaceEmbedding(model_name=Config.EmbeddingModel, trust_remote_code=True, embed_batch_size=Config.EmbedBatchSize)
storage_context = StorageContext.from_defaults(persist_dir="./index")
index = load_index_from_storage(storage_context, embed_model=embed_model)
# llm = OpenAI(model=Config.LLMModel, temperature=Config.LLMModelTemperature)
llm = AzureOpenAI(
    model=Config.LLMModel, 
    deployment_name=Config.LLMModel, 
    temperature=Config.LLMModelTemperature,
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("OPENAI_API_VERSION"))
retriever = index.as_retriever(similarity_top_k=Config.SimilarityTopK, embed_model=embed_model)
query_engine = RetrieverQueryEngine.from_args(retriever, llm=llm)

def faq_rag(query: str) -> str:
    """A function to search for answer in FAQ (Frequently Asked Questions)"""
    response = query_engine.query(query)
    return response.response
