#◾ FastAPI MongoDB CRUD Application#

A production-style FastAPI backend project implementing CRUD (Create, Read, Update, Delete) operations using MongoDB with async support via Motor.

This project demonstrates clean architecture, schema validation, and scalable API design suitable for real-world backend systems.

◾ Tech Stack

Python 3.10+

FastAPI – High-performance web framework

MongoDB – NoSQL database

Motor – Async MongoDB driver

Pydantic – Data validation

Uvicorn – ASGI server

◾ Features

✅ Create user

✅ Get all users

✅ Get user by ID

✅ Update user

✅ Delete user

✅ Async & non-blocking database operations

✅ Auto-generated Swagger UI

✅ Clean separation of concerns

✅ Production-ready structure

◾ Project Structure
fastapi_mongo_crud/
 ├── main.py        # API routes
 ├── database.py    # MongoDB connection
 ├── crud.py        # Database operations
 ├── schemas.py     # Pydantic validation schemas
 ├── models.py      # MongoDB data serializer
 ├── requirements.txt
 └── README.md

◾ Setup Instructions (Local)
1️⃣ Clone the repository
git clone https://github.com/amitnaphade21/fastapi_mongo_crud.git
cd fastapi_mongo_crud

2️⃣ Create virtual environment
python -m venv venv


Activate it:

Windows (CMD):

venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Start MongoDB

Make sure MongoDB is running on:

mongodb://localhost:27017


Run:

mongod

5️⃣ Start the FastAPI server
uvicorn main:app --reload

6️⃣ Open API Documentation (Swagger UI)

Open in browser:

http://127.0.0.1:8000/docs

◾ API Endpoints
Method	Endpoint	Description
POST	/users	Create new user
GET	/users	Get all users
GET	/users/{id}	Get user by ID
PUT	/users/{id}	Update user
DELETE	/users/{id}	Delete user
🧪 Example Request (Create User)
{
  "name": "Amit",
  "email": "amit@gmail.com",
  "age": 22
}

◾ Request Flow
Client → FastAPI → Pydantic Validation → CRUD Layer → MongoDB → Response

🏗️ Architecture Highlights

Schema validation at API layer using Pydantic

MongoDB remains schema-less but controlled via application layer

Async database operations for high performance

Clean separation between:

API layer

Business logic

Database access

◾ Environment Configuration (For Deployment)

In database.py:

import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")


This allows easy deployment to cloud (MongoDB Atlas, Render, etc.)

◾ Author

Amit Naphade

🏆 Interview Ready Statement

“This project demonstrates a scalable FastAPI backend using async MongoDB with clean architecture, schema validation, and production-ready design.”
