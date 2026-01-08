import chromadb
from chromadb.config import Settings
from config.settings import CHROMA_PATH, COLLECTION_NAME
from database.embeddings import generate_embedding

client = chromadb.Client(Settings(persist_directory=CHROMA_PATH))

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=generate_embedding
)
