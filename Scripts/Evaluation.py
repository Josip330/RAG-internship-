import os
from datetime import datetime
from tzlocal import get_localzone
from qdrant_client import QdrantClient
from langchain_ollama import OllamaEmbeddings
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

root_dir = Path(__file__).resolve().parent.parent


load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
CLUSTER_ENDPOINT = os.getenv("CLUSTER_ENDPOINT")
API_KEY = os.getenv("API_KEY")
COLLECTION = os.getenv("COLLECTION")
OPEN_API = os.getenv("OPENAI_API_KEY")




OUTPUT_FILE = root_dir / "Data" / "evaluation2_results.txt"


embedding_model = OpenAIEmbeddings()
client = QdrantClient(url=CLUSTER_ENDPOINT, api_key=API_KEY)


queries = [
    {
        "query": "Can a non creature permanent have power and toughness?",
        "subcategory": "208",
        "chunk_index": 7
    },
    {
        "query": "How do I know which rarity my card is?",
        "subcategory": "213",
        "chunk_index": 2
    },
    {
        "query": "Which supertypes are there?",
        "subcategory": "205",
        "chunk_index": 30
    },
    {
        "query": "What is mana value?",
        "subcategory": "202",
        "chunk_index": 7
    },
    {
        "query": "What is a sticker?",
        "subcategory": "123",
        "chunk_index": 1
    },
    {
        "query": "How many poison counters are needed to lose or win a game?",
        "subcategory": "122",
        "chunk_index": 6
    },
    {
        "query": "What is a counter?",
        "subcategory": "122",
        "chunk_index": 1
    },
    {
        "query": "What is the starting life total?",
        "subcategory": "118",
        "chunk_index": 31
    },
    {
        "query": "How many cards in a constructed standard deck?",
        "subcategory": "100",
        "chunk_index": 2
    },
    {
        "query": "How many mana colors are there?",
        "subcategory": "107",
        "chunk_index": 19
    }
]


total_score = 0
output_lines = []


local_time = datetime.now(get_localzone())
timestamp = local_time.strftime("%Y-%m-%d %H:%M:%S %Z")
report_header = f"""
################################################################################
### EVALUATION REPORT
### Model: {MODEL_NAME}
### Timestamp: {timestamp}
################################################################################
""".strip()

output_lines = [report_header]
total_score = 0

for i, q in enumerate(queries, 1):
    query_text = q["query"]
    expected_subcat = q["subcategory"]
    expected_index = q["chunk_index"]

    query_vector = embedding_model.embed_query(query_text)
    results = client.query_points(
        collection_name=COLLECTION,
        query=query_vector,
        limit=1,
        with_payload=True
    )

    output_lines.append(f"\nQuery {i}: {query_text}")
    if not results or not results.points:
        output_lines.append("Error: No results returned.\n" + "-" * 80)
        continue

    result = results.points[0]
    payload = result.payload
    retrieved_subcat = payload.get("subcategory")
    retrieved_index = payload.get("subcategory_index")
    snippet = payload.get("text", "")[:300]

    match_subcat = retrieved_subcat == expected_subcat
    match_index = retrieved_index == expected_index
    score = int(match_subcat) + int(match_index)
    total_score += score

    output_lines.append(f"Score: {score}/2")
    output_lines.append(f"Subcategory: Expected {expected_subcat}, Got {retrieved_subcat}")
    output_lines.append(f"Chunk Index: Expected {expected_index}, Got {retrieved_index}")
    output_lines.append(f"Top Result Snippet: {snippet}...")
    output_lines.append("-" * 80)

summary_line = f"\nTotal score: {total_score} / {len(queries) * 2}"
output_lines.append(summary_line)


output_lines.append("\n" + "=" * 80 + "\n")


for line in output_lines:
    print(line)


with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
    for line in output_lines:
        f.write(line + "\n")

