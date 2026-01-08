from fastapi import APIRouter
import uuid

from database.chroma import collection
from utils.chunking import read_docs_file, split_text
from schemas.requests import QueryRequest, UpdateRequest, DeleteRequest

router = APIRouter(prefix="/vectors", tags=["Vectors"])


@router.post("/create")
def create_vector():
    text = read_docs_file()
    chunks = split_text(text)

    stored_ids = []

    for chunk in chunks:
        doc_id = str(uuid.uuid4())

        collection.add(
            documents=[chunk],
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
    results = collection.query(
        query_texts=[request.query],
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
    collection.upsert(
        ids=[request.id],
        documents=[request.updated_text],
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
