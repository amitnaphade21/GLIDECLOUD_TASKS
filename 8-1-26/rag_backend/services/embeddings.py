import ollama
from config.settings import EMBEDDING_MODEL

def generate_embedding(text: str):
    response = ollama.embeddings(
        model=EMBEDDING_MODEL,
        prompt=text
    )
    return response["embedding"]
