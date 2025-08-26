from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from collections import defaultdict
import json
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

input_file = root_dir / "Data" / "data.txt"
output_file = root_dir / "Data" / "chunked.txt"
json_output = root_dir / "Data" / "chunks_all.json"

# Read full text
with open(input_file) as f:
    text = f.read()

# Split text into chunks
splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", " "],
    chunk_size=500,
    chunk_overlap=50,
    length_function=len
)
chunks = splitter.split_text(text)

# Extract metadata
def extract_metadata(chunk):
    # Match 3 digits + dot at start
    match = re.match(r'^(\d{3})\.', chunk.strip())
    if match:
        # Check next character after the dot
        after_dot = chunk[match.end():match.end()+1]
        if after_dot == ')':
            # This is likely a cross-reference, not a real heading
            return None, None

        subcategory = match.group(1)
        category = subcategory[0]
        return subcategory, category

    return None, None


# Assign metadata to chunks + track chunk positions in subcategories

def assign_metadata(chunks):
    meta_chunks = []
    current_sub = None
    current_cat = None

    for chunk in chunks:
        sub, cat = extract_metadata(chunk)
        if sub:
            current_sub = sub
        if cat:
            current_cat = cat

        meta_chunks.append({
            "chunk": chunk.strip(),
            "subcategory": current_sub,
            "category": current_cat,
        })

    # Count how many chunks per subcategory
    subcategory_groups = defaultdict(list)
    for chunk in meta_chunks:
        subcategory_groups[chunk["subcategory"]].append(chunk)

    # Annotate each chunk with its index in subcategory and total count
    for sub, group in subcategory_groups.items():
        total = len(group)
        for idx, chunk in enumerate(group):
            chunk["subcategory_index"] = idx + 1
            chunk["subcategory_total"] = total

    return meta_chunks

# Process and enrich
meta_chunks = assign_metadata(chunks)

# Print to console
for i, chunk in enumerate(meta_chunks, 1):
    print(f"\nChunk {i}")
    print("=" * 80)
    print(f"Category: {chunk['category']}")
    print(f"Subcategory: {chunk['subcategory']}")
    print(f"Chunk in Subcategory: {chunk['subcategory_index']} of {chunk['subcategory_total']}")
    print("\nContent:\n")
    print(chunk["chunk"])
    print("=" * 80)

# Write to file
with open(output_file, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(meta_chunks, 1):
        f.write(f"{'='*30} Chunk {i} {'='*30}\n")
        f.write(f"Category: {chunk['category']}\n")
        f.write(f"Subcategory: {chunk['subcategory']}\n")
        f.write(f"Chunk in Subcategory: {chunk['subcategory_index']} of {chunk['subcategory_total']}\n\n")
        f.write(chunk["chunk"])
        f.write("\n\n" + "="*70 + "\n\n")
        

with open(json_output, "w", encoding="utf-8") as f:
    json.dump(meta_chunks, f, indent=2, ensure_ascii=False)


print(f"Enriched chunks written to {output_file}")
