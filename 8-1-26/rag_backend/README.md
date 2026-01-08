RAG backend using Ollama and ChromaDB
What this script does

Reads text from docs.txt

Splits the text into chunks

Converts each chunk into a vector using Ollama embeddings

Stores vectors in ChromaDB

Provides APIs to:

Create vectors

Search vectors

Count vectors

Update vectors

Delete vectors

Chat using retrieved context

Tech Stack

Python

FastAPI

Ollama

ChromaDB



