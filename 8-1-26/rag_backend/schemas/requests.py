from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

class UpdateRequest(BaseModel):
    id: str
    updated_text: str

class DeleteRequest(BaseModel):
    id: str

class ChatRequest(BaseModel):
    query: str
