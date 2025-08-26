from langchain_ollama import OllamaEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct, VectorParams, Distance
import json
import uuid
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

root_dir = Path(__file__).resolve().parent.parent



MODEL_NAME = os.getenv("MODEL_NAME")
QDRANT_URL = os.getenv("QDRANT_URL")
API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION = os.getenv("QDRANT_COLLECTION_NAME")
OPENAI_API_KEY = os.getenv("OPEN_API")
EMBEDDINGS_MODEL_NAME = os.getenv("EMBEDDINGS_MODEL_NAME")
DIMENSION = 1536
DATA = root_dir / "Data" / "chunks_all.json"


with open(DATA, "r", encoding="utf-8") as f:
    meta_chunks = json.load(f)

embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

qdrant = QdrantClient(
    url = QDRANT_URL,
    api_key = API_KEY,
    timeout=60
)


qdrant.delete_collection(COLLECTION)

if not qdrant.collection_exists(COLLECTION):
    qdrant.create_collection(
        collection_name=COLLECTION,
        vectors_config=VectorParams(size=DIMENSION, distance=Distance.COSINE),
    )


batch = []
for idx, chunk in enumerate(meta_chunks):
    text = chunk["chunk"]
    vector = embedding_model.embed_query(text)

    point = PointStruct(
        id=str(uuid.uuid4()),
        vector=vector,
        payload={
            "text": text,
            "category": chunk["category"],
            "subcategory": chunk["subcategory"],
            "subcategory_index": chunk.get("subcategory_index"),
            "subcategory_total": chunk.get("subcategory_total"),
        },
    )
    batch.append(point)


from tqdm import tqdm

BATCH_SIZE = 100
total = len(batch)

for i in tqdm(range(0, total, BATCH_SIZE), desc="Uploading batches"):
    sub_batch = batch[i:i + BATCH_SIZE]
    qdrant.upsert(collection_name=COLLECTION, points=sub_batch)

print(f"Uploaded {total} chunks to Qdrant collection '{COLLECTION}' in batches of {BATCH_SIZE}.")
