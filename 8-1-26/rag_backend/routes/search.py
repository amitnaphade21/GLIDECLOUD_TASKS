from fastapi import APIRouter
from database.retriever import search_chunks

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
def search(query: str, k: int = 5):
    results = search_chunks(query, k)
    return {
        "query": query,
        "top_k": k,
        "results": results
    }
