from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOpenAI(model="gpt-4o-mini", temperature=0)

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def get_qdrant_client():
    return QdrantClient(
        url=os.getenv("QDRANT_URL"),
        api_key=os.getenv("QDRANT_API_KEY"),
    )