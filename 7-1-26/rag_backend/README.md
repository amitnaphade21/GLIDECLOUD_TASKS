# 🚀 RAG Backend - Vector Search API

A powerful **Retrieval Augmented Generation (RAG)** backend built with FastAPI, ChromaDB, and Ollama. This service enables semantic search, document embedding, and retrieval capabilities with local LLM support.

---

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Project Architecture](#project-architecture)

---

## ✨ Features

- **Document Embedding**: Convert text documents into vector embeddings using Ollama
- **Vector Storage**: Persistent storage using ChromaDB
- **Semantic Search**: Query similar documents using semantic similarity
- **CRUD Operations**: Create, read, update, and delete vector embeddings
- **RESTful API**: Built with FastAPI for easy integration
- **Local LLM**: Uses local Ollama models (no external API keys needed)
- **Chunking Strategy**: Intelligent text chunking for better embeddings

---

## 📁 Project Structure

```
rag_backend/
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── docs.txt                        # Source documents for embedding
├── chroma_vectors.json             # Vector metadata export
├── config/
│   ├── settings.py                # Configuration settings
│   └── __pycache__/
├── database/
│   ├── chroma.py                  # ChromaDB connection and collection
│   └── __pycache__/
├── routes/
│   ├── vectors.py                 # Vector API endpoints
│   └── __pycache__/
├── services/
│   ├── embeddings.py              # Ollama embedding generation
│   ├── llm.py                     # LLM chat functionality
│   └── __pycache__/
├── schemas/
│   ├── requests.py                # Pydantic request models
│   └── __pycache__/
├── utils/
│   ├── chunking.py                # Text chunking utilities
│   └── __pycache__/
├── tests/
│   ├── test_chroma_storage.py     # ChromaDB storage tests
│   ├── test_health.py             # Health check tests
│   ├── test_vector_store.py       # Vector store tests
│   ├── test_vectors.py            # Vector endpoint tests
│   └── __pycache__/
├── chroma_db/                      # ChromaDB persistent storage
└── output_Screenshots/             # Testing and documentation screenshots
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend Framework** | FastAPI | RESTful API development |
| **Server** | Uvicorn | ASGI application server |
| **Vector Database** | ChromaDB | Vector storage and similarity search |
| **Embeddings** | Ollama | Local embedding generation |
| **LLM** | Ollama (TinyLLaMA) | Local language model |
| **Data Validation** | Pydantic | Request/response validation |
| **Language** | Python 3.8+ | Core programming language |

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8** or higher
- **Ollama** ([Download here](https://ollama.ai))
- **pip** (Python package manager)
- **Git** (optional, for version control)

### Verify Installations

```bash
python --version
pip --version
ollama --version
```

---

## 🔧 Installation

### Step 1: Clone or Navigate to the Project

```bash
# If cloning from repository
git clone <your-repo-url>
cd rag_backend

# Or navigate to existing directory
cd c:\Users\user\Desktop\GLIDECLOUD\GLIDECLOUD_TASKS\7-1-26\rag_backend
```

### Step 2: Create Virtual Environment (Recommended)

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Pull Required Ollama Models

```bash
ollama pull nomic-embed-text
ollama pull tinyllama
```

---

## ⚙️ Configuration

Edit `config/settings.py` to customize your setup:

```python
import os

CHROMA_PATH = "./chroma_db"              # ChromaDB storage location
COLLECTION_NAME = "knowledge_base"       # Collection name
EMBEDDING_MODEL = "nomic-embed-text"     # Embedding model
LLM_MODEL = "tinyllama"                  # Language model
DOCS_PATH = "docs.txt"                   # Source documents path
```

**Update documents:** Edit `docs.txt` with your content.

---

## 🚀 Running the Server

### Start Ollama Service (in separate terminal)

**Windows:**
```powershell
ollama serve
```

**Linux/macOS:**
```bash
ollama serve
```

### Start FastAPI Server

**Windows (PowerShell):**
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Linux/macOS:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Access the Server

- **API**: http://localhost:8000
- **Interactive Docs (Swagger UI)**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

## 📡 API Endpoints

### 1. Create/Embed Documents
**POST** `/vectors/create`

Embeds documents from `docs.txt` and stores vectors in ChromaDB.

```bash
curl -X POST http://localhost:8000/vectors/create
```

**Response:**
```json
{
  "message": "Documents embedded and stored successfully",
  "chunks_stored": 5,
  "document_ids": ["uuid-1", "uuid-2", "uuid-3", "uuid-4", "uuid-5"]
}
```

---

### 2. Search Vectors
**POST** `/vectors/read`

Retrieve similar documents based on semantic similarity.

```bash
curl -X POST http://localhost:8000/vectors/read \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
```

**Request Body:**
```json
{
  "query": "Your search query"
}
```

**Response:**
```json
{
  "query": "What is machine learning?",
  "results": [
    {
      "document": "Machine learning is a subset of artificial intelligence...",
      "metadata": {"source": "docs.txt"},
      "distance": 0.1234
    }
  ]
}
```

---

### 3. Count Vectors
**GET** `/vectors/count`

Get the total number of stored vectors.

```bash
curl -X GET http://localhost:8000/vectors/count
```

**Response:**
```json
{
  "count": 15
}
```

---

### 4. Update Vector
**POST** `/vectors/update`

Update an existing vector document.

```bash
curl -X POST http://localhost:8000/vectors/update \
  -H "Content-Type: application/json" \
  -d '{"id": "document-uuid", "updated_text": "Updated content here"}'
```

**Request Body:**
```json
{
  "id": "document-uuid",
  "updated_text": "Your updated document content"
}
```

**Response:**
```json
{
  "message": "Document updated successfully"
}
```

---

### 5. Delete Vector
**POST** `/vectors/delete`

Remove a vector from the database.

```bash
curl -X POST http://localhost:8000/vectors/delete \
  -H "Content-Type: application/json" \
  -d '{"id": "document-uuid"}'
```

**Request Body:**
```json
{
  "id": "document-uuid"
}
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

---

## 💡 Usage Examples

### Python Example

```python
import requests

BASE_URL = "http://localhost:8000"

# Create vectors
response = requests.post(f"{BASE_URL}/vectors/create")
print(response.json())

# Search vectors
search_data = {"query": "machine learning"}
response = requests.post(f"{BASE_URL}/vectors/read", json=search_data)
print(response.json())

# Count vectors
response = requests.get(f"{BASE_URL}/vectors/count")
print(response.json())
```

### Bash Script Example

```bash
#!/bin/bash

API_URL="http://localhost:8000"

# Create embeddings
echo "Creating embeddings..."
curl -X POST "$API_URL/vectors/create"

# Search
echo -e "\n\nSearching vectors..."
curl -X POST "$API_URL/vectors/read" \
  -H "Content-Type: application/json" \
  -d '{"query": "AI and machine learning"}'

# Count
echo -e "\n\nCounting vectors..."
curl -X GET "$API_URL/vectors/count"
```

---

## 🏗️ Project Architecture

### Data Flow

```
docs.txt
    ↓
[Chunking] (utils/chunking.py)
    ↓
Text Chunks
    ↓
[Embedding Service] (services/embeddings.py)
    ↓
Vectors (via Ollama)
    ↓
[ChromaDB] (database/chroma.py)
    ↓
Persistent Vector Storage
```

### Request Flow

```
HTTP Request
    ↓
[FastAPI Route] (routes/vectors.py)
    ↓
[Service Layer] (services/)
    ↓
[Database Layer] (database/)
    ↓
[ChromaDB Instance]
    ↓
JSON Response
```

### Key Modules

- **main.py**: FastAPI app initialization and routing
- **config/settings.py**: Configuration management
- **routes/vectors.py**: API endpoint definitions
- **services/embeddings.py**: Ollama embedding generation
- **services/llm.py**: LLM chat functionality
- **database/chroma.py**: ChromaDB connection and CRUD
- **utils/chunking.py**: Document parsing and chunking
- **schemas/requests.py**: Request validation models

---

## 🧪 Testing

Run the included test suite:

```bash
pytest tests/ -v
```

Individual test files:
```bash
pytest tests/test_health.py -v
pytest tests/test_vector_store.py -v
pytest tests/test_vectors.py -v
```

---

## 📝 License

This project is part of GLIDECLOUD.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 standards
- All tests pass before submitting
- Update documentation for new features

---

## ⚠️ Troubleshooting

### Ollama Connection Error
```bash
# Ensure Ollama is running
ollama serve

# Check if Ollama is accessible
curl http://localhost:11434
```

### ChromaDB Path Error
```bash
# Ensure chroma_db directory exists
mkdir chroma_db

# Check permissions
ls -la chroma_db
```

### Port Already in Use
```bash
# Use a different port
uvicorn main:app --port 8001
```

### Virtual Environment Issues
```bash
# Deactivate and recreate
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
```

---





