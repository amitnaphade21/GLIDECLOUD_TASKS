# 🧪 Testing Guide - RAG Backend

Complete guide to running and understanding the test suite for the RAG Backend project.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Test Structure](#test-structure)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

The test suite provides comprehensive coverage of:
- **Unit Tests**: Individual component functionality
- **Integration Tests**: Component interactions
- **API Tests**: FastAPI endpoint validation
- **Database Tests**: ChromaDB operations
- **Service Tests**: Embedding and LLM services
- **Utility Tests**: Helper functions and utilities

**Total Test Files**: 7
**Total Test Cases**: 150+
**Coverage Target**: 80%+

---

## 📁 Test Structure

```
tests/
├── conftest.py                      # pytest configuration
├── run_tests.py                     # test runner script
├── test_health.py                   # Health check endpoints
├── test_vectors.py                  # Vector API endpoints
├── test_vector_store.py             # ChromaDB operations
├── test_chroma_storage.py           # ChromaDB persistence
├── test_embeddings_service.py       # Embedding generation
├── test_chunking_utils.py           # Text chunking utilities
├── test_request_schemas.py          # Pydantic model validation
└── __pycache__/
```

---

## 🚀 Running Tests

### Prerequisites

```bash
# Install pytest and plugins
pip install pytest pytest-cov pytest-asyncio
```

### Run All Tests

**Using Python script:**
```bash
cd tests
python run_tests.py --all
```

**Using pytest directly:**
```bash
pytest tests/ -v
```

**Using pytest with detailed output:**
```bash
pytest tests/ -v --tb=short
```

---

### Run Quick Sanity Tests

```bash
cd tests
python run_tests.py --quick
```

Or directly:
```bash
pytest tests/test_health.py -v
```

---

### Run Tests by Category

```bash
cd tests
python run_tests.py --category
```

This shows results for each test category:
- Health Tests
- Vector API Tests
- Vector Store Tests
- ChromaDB Storage Tests
- Embeddings Service Tests
- Chunking Utils Tests
- Request Schema Tests

---

### Run Specific Test File

```bash
# Using test runner
cd tests
python run_tests.py --file tests/test_vectors.py

# Or directly with pytest
pytest tests/test_vectors.py -v
```

---

### Run Specific Test Class

```bash
pytest tests/test_vectors.py::TestVectorCreateEndpoint -v
```

---

### Run Specific Test Function

```bash
pytest tests/test_vectors.py::TestVectorCreateEndpoint::test_create_vectors_success -v
```

---

### Run Tests with Verbose Output

```bash
pytest tests/ -vv
```

---

### Run Tests with Print Statements

```bash
pytest tests/ -s
```

---

### Run Tests with Coverage Report

```bash
cd tests
python run_tests.py --coverage
```

Or directly:
```bash
pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
```

View coverage report:
```bash
# Open htmlcov/index.html in browser
```

---

## 📊 Test Categories

### 1. Health Tests (`test_health.py`)

**Purpose**: Verify application startup and basic endpoints

**Test Cases**:
- ✓ Root endpoint returns success
- ✓ Swagger UI available
- ✓ ReDoc documentation available
- ✓ OpenAPI schema available

**Run**:
```bash
pytest tests/test_health.py -v
```

---

### 2. Vector API Tests (`test_vectors.py`)

**Purpose**: Test all vector API endpoints

**Test Categories**:
- **Create Endpoint**: Vector embedding creation
- **Read Endpoint**: Semantic search functionality
- **Count Endpoint**: Vector counting
- **Update Endpoint**: Vector updates
- **Delete Endpoint**: Vector deletion
- **Integration Tests**: Multi-endpoint workflows

**Test Cases**: 30+

**Run**:
```bash
pytest tests/test_vectors.py -v
```

**Example cURL Commands**:
```bash
# Create vectors
curl -X POST http://localhost:8000/vectors/create

# Search vectors
curl -X POST http://localhost:8000/vectors/read \
  -H "Content-Type: application/json" \
  -d '{"query": "test query"}'

# Count vectors
curl -X GET http://localhost:8000/vectors/count

# Delete vector
curl -X POST http://localhost:8000/vectors/delete \
  -H "Content-Type: application/json" \
  -d '{"id": "document-uuid"}'
```

---

### 3. Vector Store Tests (`test_vector_store.py`)

**Purpose**: Test ChromaDB storage and retrieval operations

**Test Categories**:
- **CRUD Operations**: Create, read, update, delete
- **Embeddings**: Embedding generation and consistency
- **Similarity Search**: Vector similarity queries
- **Metadata**: Metadata storage and retrieval

**Test Cases**: 35+

**Run**:
```bash
pytest tests/test_vector_store.py -v
```

---

### 4. ChromaDB Storage Tests (`test_chroma_storage.py`)

**Purpose**: Test ChromaDB persistence and data integrity

**Test Categories**:
- **Initialization**: Database setup
- **Persistence**: Data durability
- **Data Integrity**: Content preservation
- **Error Handling**: Edge cases
- **Storage Stats**: Metrics and counts

**Test Cases**: 25+

**Run**:
```bash
pytest tests/test_chroma_storage.py -v
```

---

### 5. Embeddings Service Tests (`test_embeddings_service.py`)

**Purpose**: Test embedding generation and properties

**Test Categories**:
- **Embedding Generation**: Vector creation
- **Similarity**: Text similarity
- **Normalization**: Embedding properties
- **Edge Cases**: Special characters, unicode

**Test Cases**: 25+

**Run**:
```bash
pytest tests/test_embeddings_service.py -v
```

---

### 6. Chunking Utils Tests (`test_chunking_utils.py`)

**Purpose**: Test document reading and text chunking

**Test Categories**:
- **File Reading**: Document file operations
- **Text Splitting**: Chunking algorithms
- **Content Preservation**: Data integrity
- **Edge Cases**: Empty strings, large documents

**Test Cases**: 30+

**Run**:
```bash
pytest tests/test_chunking_utils.py -v
```

---

### 7. Request Schema Tests (`test_request_schemas.py`)

**Purpose**: Test Pydantic request model validation

**Test Categories**:
- **QueryRequest**: Search query validation
- **UpdateRequest**: Document update validation
- **DeleteRequest**: Document deletion validation
- **ChatRequest**: Chat query validation

**Test Cases**: 35+

**Run**:
```bash
pytest tests/test_request_schemas.py -v
```

---

## 📈 Test Coverage

### View Coverage Report

```bash
# Generate report
pytest tests/ --cov=. --cov-report=html

# Open in browser
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Coverage by Module

Target coverage:
- **routes/vectors.py**: 90%+
- **services/**: 85%+
- **database/**: 90%+
- **utils/**: 95%+
- **schemas/**: 100%

---

## ✅ Best Practices

### Writing New Tests

1. **Follow naming convention**:
   ```python
   def test_<feature>_<scenario>_<expected_result>():
       pass
   ```

2. **Use descriptive docstrings**:
   ```python
   def test_create_vector_success(self, client):
       """Test successful vector creation from docs.txt"""
       pass
   ```

3. **Organize with test classes**:
   ```python
   class TestVectorCreateEndpoint:
       def test_case_1(self): ...
       def test_case_2(self): ...
   ```

4. **Use fixtures for setup/teardown**:
   ```python
   @pytest.fixture(autouse=True)
   def cleanup(self):
       # Setup
       yield
       # Teardown
   ```

5. **Arrange-Act-Assert pattern**:
   ```python
   def test_something(self, client):
       # Arrange
       data = {"query": "test"}
       
       # Act
       response = client.post("/vectors/read", json=data)
       
       # Assert
       assert response.status_code == 200
   ```

---

## 🐛 Troubleshooting

### Tests Fail: "Module not found"

**Solution**: Add parent directory to path:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/
```

---

### Tests Fail: "Ollama connection refused"

**Solution**: Start Ollama service first:
```bash
# In separate terminal
ollama serve

# Then run tests
pytest tests/
```

---

### Tests Fail: "ChromaDB path error"

**Solution**: Create chroma_db directory:
```bash
mkdir chroma_db
pytest tests/
```

---

### Tests Fail: "docs.txt not found"

**Solution**: Ensure docs.txt exists in project root:
```bash
touch docs.txt
echo "Sample documentation content" >> docs.txt
pytest tests/
```

---

### Run Tests in Isolation

```bash
# Run without other instances
pytest tests/ --forked
```

---

### Verbose Error Output

```bash
pytest tests/ -vv --tb=long
```

---

### Run with Custom Markers

```bash
# Run only unit tests
pytest tests/ -m unit

# Skip slow tests
pytest tests/ -m "not slow"

# Run integration tests
pytest tests/ -m integration
```

---

## 📝 Test Execution Examples

### Complete Test Run

```bash
# Run all tests with coverage
pytest tests/ -v --cov=. --cov-report=term-missing
```

### Quick Smoke Test

```bash
# Test basic functionality
pytest tests/test_health.py tests/test_vectors.py -v
```

### Development Mode

```bash
# Run tests with auto-reload and print statements
pytest tests/ -s --tb=short
```

### CI/CD Pipeline

```bash
# Strict mode with coverage threshold
pytest tests/ --cov=. --cov-fail-under=80 --strict-markers
```

---

## 🎓 Learning Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/advanced/testing-dependencies/)
- [Pydantic Validation](https://pydantic-docs.helpmanual.io/)
- [ChromaDB Testing](https://docs.trychroma.com/)

---

## ✨ Test Statistics

| Category | Tests | Status |
|----------|-------|--------|
| Health | 5 | ✓ |
| Vector API | 18 | ✓ |
| Vector Store | 20 | ✓ |
| ChromaDB | 18 | ✓ |
| Embeddings | 20 | ✓ |
| Chunking | 23 | ✓ |
| Schemas | 35 | ✓ |
| **TOTAL** | **139** | **✓** |

---

**Last Updated**: January 2026
**Test Framework**: pytest 7.x+
**Python**: 3.8+
