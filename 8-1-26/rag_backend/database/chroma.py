import chromadb
from config.settings import CHROMA_PATH, COLLECTION_NAME

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)