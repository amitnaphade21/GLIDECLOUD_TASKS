from fastapi import APIRouter
import uuid

from database.chroma import collection
from services.embeddings import generate_embedding
from utils.chunking import read_docs_file, split_text
from schemas.requests import QueryRequest, UpdateRequest, DeleteRequest

router = APIRouter(prefix="/vectors", tags=["Vectors"])


@router.post("/create")
def create_vector():
    text = read_docs_file()
    chunks = split_text(text)

    stored_ids = []

    for chunk in chunks:
        embedding = generate_embedding(chunk)
        doc_id = str(uuid.uuid4())

        collection.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[doc_id],
            metadatas=[{"source": "docs.txt"}]
        )

        stored_ids.append(doc_id)

    return {
        "message": "Documents embedded and stored successfully",
        "chunks_stored": len(stored_ids),
        "document_ids": stored_ids
    }


@router.post("/read")
def read_vectors(request: QueryRequest):
    query_embedding = generate_embedding(request.query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    response = []

    for i in range(len(results["documents"][0])):
        response.append({
            "document": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i]
        })

    return {
        "query": request.query,
        "results": response
    }


@router.post("/update")
def update_vector(request: UpdateRequest):
    new_embedding = generate_embedding(request.updated_text)

    collection.upsert(
        ids=[request.id],
        documents=[request.updated_text],
        embeddings=[new_embedding],
        metadatas=[{"source": "docs.txt", "type": "updated"}]
    )

    return {"message": "Document updated successfully"}


@router.get("/count")
def count_vectors():
    return {"count": collection.count()}


@router.post("/delete")
def delete_vector(request: DeleteRequest):
    collection.delete(ids=[request.id])
    return {"message": "Document deleted successfully"}
