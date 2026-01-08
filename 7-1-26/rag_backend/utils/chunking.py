import os
from config.settings import DOCS_PATH

def read_docs_file():
    if not os.path.exists(DOCS_PATH):
        raise Exception("docs.txt file not found")

    with open(DOCS_PATH, "r", encoding="utf-8") as f:
        return f.read()

def split_text(text, chunk_size=40):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunks.append(" ".join(current))
            current = []

    if current:
        chunks.append(" ".join(current))

    return chunks
