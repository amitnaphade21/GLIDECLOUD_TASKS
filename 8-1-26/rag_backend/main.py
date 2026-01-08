from fastapi import FastAPI
from routes import vectors, search
from database.retriever import search_chunks

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = FastAPI(title="RAG API with Chroma")

app.include_router(vectors.router)
app.include_router(search.router)


@app.get("/")
def root():
    return {"status": "RAG API running"}

