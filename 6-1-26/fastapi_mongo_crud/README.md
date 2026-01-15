# FastAPI MongoDB CRUD Application

A production-grade REST API backend implementing CRUD operations for user management using MongoDB with async/await support. This project demonstrates clean architecture, modular organization, and best practices for scalable API development.

## Technology Stack

- **Python** 3.11+
- **FastAPI** 0.128+ - Modern, fast web framework with automatic API documentation
- **MongoDB** - NoSQL database for flexible data storage
- **Motor** 3.7+ - Asynchronous MongoDB driver for non-blocking I/O
- **Pydantic** 2.12+ - Data validation and serialization using Python type hints
- **Uvicorn** 0.40+ - ASGI server for running the application
- **PyMongo** 4.16+ - Python driver for MongoDB

## Project Structure

```
fastapi_mongo_crud/
├── app/
│   ├── core/
│   │   └── database.py          # MongoDB connection configuration
│   ├── models/
│   │   └── user.py              # User helper functions and transformations
│   ├── schemas/
│   │   └── user.py              # Pydantic models for request/response validation
│   ├── crud/
│   │   └── user.py              # Database operation functions
│   └── routes/
│       └── user.py              # API endpoint definitions
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
```

## Features

- Full CRUD operations for user management
- Asynchronous database operations with Motor for high performance
- Request/response validation using Pydantic models
- ObjectId support for MongoDB document identification
- Automatic API documentation with Swagger UI
- Error handling with appropriate HTTP status codes
- Clean separation of concerns with organized folder structure
- Support for partial updates with optional fields

## Prerequisites

- Python 3.11 or higher
- MongoDB 4.0 or higher running on localhost:27017
- pip package manager

## Installation and Setup

### 1. Clone or download the project

```bash
cd fastapi_mongo_crud
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install fastapi uvicorn motor pydantic pymongo
```

## Running the Application

### Start the server with auto-reload

```bash
uvicorn main:app --reload
```

The server will start on http://127.0.0.1:8000

### Access the API

- **Interactive API Documentation (Swagger UI)**: http://127.0.0.1:8000/docs
- **Alternative API Documentation (ReDoc)**: http://127.0.0.1:8000/redoc
- **Root Endpoint**: http://127.0.0.1:8000/

## API Endpoints

### 1. Create a User

```bash
curl -X POST http://127.0.0.1:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "age": 28
  }'
```

### 2. Get All Users

```bash
curl http://127.0.0.1:8000/users
```

### 3. Get User by ID

```bash
curl http://127.0.0.1:8000/users/{user_id}
```

Replace `{user_id}` with the actual MongoDB ObjectId.

### 4. Update a User

```bash
curl -X PUT http://127.0.0.1:8000/users/{user_id} \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "age": 30
  }'
```

### 5. Delete a User

```bash
curl -X DELETE http://127.0.0.1:8000/users/{user_id}
```

## Response Examples

### Success Response

```json
{
  "id": "507f1f77bcf86cd799439011",
  "name": "John Doe",
  "email": "john@example.com",
  "age": 28
}
```

### Error Response

```json
{
  "detail": "User not found"
}
```

## Troubleshooting

### MongoDB Connection Error

Ensure MongoDB is running on your system:

**On Windows:**
```bash
mongod
```

**On macOS:**
```bash
brew services start mongodb-community
```

**On Linux:**
```bash
sudo systemctl start mongod
```

### Port Already in Use

If port 8000 is already in use, specify a different port:

```bash
uvicorn main:app --reload --port 8001
```

### Virtual Environment Issues

To deactivate the virtual environment:

```bash
deactivate
```

## Development Notes

- The application uses async/await for all database operations ensuring non-blocking I/O
- Pydantic models handle both request validation and response serialization
- ObjectId conversion is handled automatically for MongoDB compatibility
- All timestamps and database operations are managed by Motor's async interface

## License

This project is provided as-is for educational and development purposes.


