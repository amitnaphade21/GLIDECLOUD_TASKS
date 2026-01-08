from fastapi import FastAPI
from routes import vectors

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
app = FastAPI(title="RAG API with Chroma")

app.include_router(vectors.router)



@app.get("/")
def root():
    return {"status": "RAG API running"}
