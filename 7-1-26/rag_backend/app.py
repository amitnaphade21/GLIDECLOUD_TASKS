from fastapi import FastAPI
from pydantic import BaseModel
import chromadb
import ollama
import uuid
import os

app = FastAPI()

chroma_client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma_client.get_or_create_collection(
    name="knowledge_base"
)

class QueryRequest(BaseModel):
    query: str

class UpdateRequest(BaseModel):
    id: str
    updated_text: str

class DeleteRequest(BaseModel):
    id: str

class ChatRequest(BaseModel):
    query: str


def generate_embedding(text: str):
    response = ollama.embeddings(
        model="nomic-embed-text",
        prompt=text
    )
    return response["embedding"]


def read_docs_file():
    if not os.path.exists("docs.txt"):
        raise Exception("docs.txt file not found")

    with open("docs.txt", "r", encoding="utf-8") as f:
        return f.read()


def split_text(text, chunk_size=500):
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


@app.post("/create")
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
            metadatas=[{
                "source": "docs.txt"
            }]
        )

        stored_ids.append(doc_id)

    return {
        "message": "Documents embedded and stored successfully",
        "chunks_stored": len(stored_ids),
        "document_ids": stored_ids
    }


@app.post("/read")
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


@app.post("/update")
def update_vector(request: UpdateRequest):
    new_embedding = generate_embedding(request.updated_text)

    collection.upsert(
        ids=[request.id],
        documents=[request.updated_text],
        embeddings=[new_embedding],
        metadatas=[{
            "source": "docs.txt",
            "type": "updated"
        }]
    )

    return {
        "message": "Document updated successfully",
        "document_id": request.id
    }


@app.get("/count")
def count_vectors():
    return {
        "count": collection.count()
    }


@app.post("/delete")
def delete_vector(request: DeleteRequest):
    collection.delete(
        ids=[request.id]
    )

    return {
        "message": "Document deleted successfully",
        "document_id": request.id
    }


def generate_answer(context: str, question: str):
    prompt = f"""
Based on the context below, answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.generate(
        model="tinyllama",
        prompt=prompt
    )

    return response["response"]


@app.post("/chat")
def chat(request: ChatRequest):
    query_embedding = generate_embedding(request.query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    context = "\n\n".join(documents)

    answer = generate_answer(context, request.query)

    return {
        "query": request.query,
        "answer": answer.strip(),
        "sources": metadatas
    }
