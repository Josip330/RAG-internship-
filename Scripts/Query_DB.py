from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaEmbeddings
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import OpenAIEmbeddings

load_dotenv()

# Qdrant setup parameters (use your own values)
MODEL_NAME = os.getenv("MODEL_NAME")
CLUSTER_ENDPOINT = os.getenv("CLUSTER_ENDPOINT")
API_KEY = os.getenv("API_KEY")
COLLECTION = os.getenv("COLLECTION")
OPEN_API = os.getenv("OPENAI_API_KEY")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME")

# Initialize Qdrant client
qdrant_client = QdrantClient(url=CLUSTER_ENDPOINT, api_key=API_KEY)

# Initialize embedding model
embedding_model = OpenAIEmbeddings()

# Create Qdrant vector store interface
vector_store = QdrantVectorStore(
    client=qdrant_client,
    collection_name=COLLECTION,
    embedding=embedding_model,
    content_payload_key="text"  # adjust if your text is stored under another key
)

# Create retriever, set number of results to retrieve (k)
retriever = vector_store.as_retriever(search_kwargs={"k": 4})

def query_database(question: str):
    # Retrieve top k documents from the vector store
    docs = retriever.invoke(question)
    
    # Extract the text content from the retrieved docs
    results = []
    for doc in docs:
        # doc.metadata contains stored metadata, doc.page_content is fallback content
        text = doc.metadata.get("text", doc.page_content)
        results.append(text)
    
    return results

# Example usage:
if __name__ == "__main__":
    question = "How many mana colors are there?"
    retrieved_texts = query_database(question)
    print("Retrieved contexts:")
    for i, text in enumerate(retrieved_texts, 1):
        print(f"{i}. {text}\n")
