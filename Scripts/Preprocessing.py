import pymupdf
import unicodedata
import fitz
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent


input_file = root_dir / "Data" / "MagicCompRules 20250404.pdf"
output_file = root_dir / "Data" / "data.txt"
start_page = 4  # page 5 (0-based)
end_page = 245  # page 246 (0-based)

# Map of common "fancy" unicode characters to their plain equivalents
replacement_map = {
    "": "\n",
    "“": '"',
    "”": '"',
    "’": "'",
    "\n \n": "\n\n"
}

def normalize_text(text):
    for bad_char, good_char in replacement_map.items():
        text = text.replace(bad_char, good_char)
    return unicodedata.normalize("NFKC", text)

doc = fitz.open(input_file)

with open(output_file, "w", encoding="utf-8") as out:
    for page_num in range(start_page, end_page + 1):
        page = doc[page_num]
        text = page.get_text()
        text = normalize_text(text)
        out.write(text.strip())

