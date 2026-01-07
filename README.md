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

Setup

Install Ollama and run:

ollama serve
ollama pull nomic-embed-text
ollama pull tinyllama


Create virtual environment and install dependencies:

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt


Run the script:

python -m uvicorn app:app --reload


Open in browser:

http://127.0.0.1:8000/docs

How to use

Call POST /create to read docs.txt and store vectors

Call GET /count to see number of stored vectors

Call POST /read to search using a query

Call POST /chat to ask questions from the document

Call POST /update to update a stored vector

Call POST /delete to delete a vector
