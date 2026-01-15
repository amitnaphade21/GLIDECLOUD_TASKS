# 🚀 RAG Backend - Retrieval Augmented Generation API

> A powerful REST API for semantic document retrieval using Ollama embeddings and ChromaDB vector storage.

---

## 📋 Overview

This project implements a **Retrieval Augmented Generation (RAG)** backend that enables semantic search and intelligent document retrieval. It combines the power of **Ollama** for embeddings and **ChromaDB** for efficient vector storage, providing a complete solution for building knowledge-base applications.

### ✨ Key Features

- 📄 **Document Processing**: Automatically reads and chunks documents from text files
- 🔗 **Semantic Embeddings**: Converts text chunks into high-dimensional vectors using Ollama
- 🗄️ **Vector Storage**: Persists embeddings in ChromaDB with metadata support
- 🔍 **Smart Search**: Retrieve semantically similar documents with configurable result limits
- 🔄 **Full CRUD Operations**: Create, read, update, and delete vectors
- ⚡ **RESTful API**: Clean, intuitive endpoints built with FastAPI
- 🧪 **Test Coverage**: Comprehensive test suite for reliability

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Framework** | FastAPI |
| **Server** | Uvicorn |
| **Vector DB** | ChromaDB |
| **Embeddings** | Ollama |
| **Validation** | Pydantic |
| **API Format** | REST/JSON |

---

## 📦 Installation

### Prerequisites
- Python 3.8+
- Ollama installed and running ([Download](https://ollama.ai))

### Setup

1. **Clone the repository** and navigate to the project directory:
```bash
cd rag_backend
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Verify Ollama is running**:
```bash
ollama serve
```

4. **Add your documents** to `docs.txt` in the project root

---

## 🚀 Quick Start

### Run the API Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Interactive Documentation

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 📚 API Endpoints

### Vector Management

#### Create Vectors from Documents
```
POST /vectors/create
```
Reads documents from `docs.txt`, chunks them, and stores embeddings.

**Response:**
```json
{
  "message": "Documents embedded and stored successfully",
  "chunks_stored": 10,
  "document_ids": ["id1", "id2", ...]
}
```

#### Read Vectors
```
POST /vectors/read
```
Retrieve stored vectors with metadata.

**Request Body:**
```json
{
  "query": "search text"
}
```

### Search

#### Semantic Search
```
GET /search?query=your%20query&k=5
```
Search for semantically similar documents.

**Parameters:**
- `query` (string): Search query
- `k` (integer, default: 5): Number of results to return

**Response:**
```json
{
  "query": "your query",
  "top_k": 5,
  "results": [
    {
      "text": "document content",
      "metadata": {"source": "docs.txt"},
      "score": 0.15
    }
  ]
}
```

### Health Check
```
GET /
```
Check API status.

---

## 📁 Project Structure

```
rag_backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Project dependencies
├── docs.txt               # Source documents for embedding
├── config/                # Configuration settings
│   └── settings.py        # App configuration
├── database/              # Database layer
│   ├── chroma.py         # ChromaDB client initialization
│   └── retriever.py      # Search and retrieval functions
├── routes/                # API endpoints
│   ├── vectors.py        # Vector operations endpoints
│   └── search.py         # Search endpoints
├── services/              # Business logic
│   ├── embeddings.py     # Ollama embedding service
│   └── llm.py            # LLM interactions
├── schemas/               # Pydantic request/response models
│   └── requests.py       # Request validation schemas
├── utils/                 # Utility functions
│   └── chunking.py       # Text splitting and processing
├── tests/                 # Test suite
│   ├── test_health.py    # Health check tests
│   └── test_chroma_storage.py  # Storage tests
└── chroma_db/            # ChromaDB persistence directory
```

---

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test file:
```bash
pytest tests/test_health.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=./ --cov-report=html
```

### Test Coverage

- ✅ API health checks
- ✅ Vector storage operations
- ✅ Semantic search functionality
- ✅ Error handling and validation
- ✅ Data persistence

---

## ⚙️ Configuration

Edit `config/settings.py` to customize:

- `EMBEDDING_MODEL`: Ollama model to use (default: `nomic-embed-text`)
- `CHROMA_PATH`: Path to ChromaDB persistence directory
- `COLLECTION_NAME`: ChromaDB collection name
- `CHUNK_SIZE`: Document chunk size for splitting
- `CHUNK_OVERLAP`: Overlap between chunks

---

## 🔄 Workflow Example

1. **Add documents** to `docs.txt`
2. **Create embeddings**:
   ```bash
   curl -X POST http://localhost:8000/vectors/create
   ```
3. **Search documents**:
   ```bash
   curl http://localhost:8000/search?query=your%20question&k=3
   ```
4. **Retrieve results** with semantic relevance scores

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama connection failed | Ensure Ollama is running: `ollama serve` |
| ChromaDB not found | Check `CHROMA_PATH` in settings |
| Port 8000 in use | Change port: `uvicorn main:app --port 8001` |
| Module not found | Install dependencies: `pip install -r requirements.txt` |

---

## 📝 License

This project is part of the GLIDECLOUD initiative.

---

## 🤝 Contributing

Contributions are welcome! Please ensure:
- Code follows PEP 8 style guidelines
- All tests pass
- New features include test coverage
- Documentation is updated

---

## 📞 Support

For issues or questions, please refer to the project documentation or contact the development team.

**Last Updated**: January 2026



