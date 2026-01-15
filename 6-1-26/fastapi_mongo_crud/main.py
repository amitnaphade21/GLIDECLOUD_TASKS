from fastapi import FastAPI
from app.routes.user import router as user_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI Mongo CRUD Running"}

# Include routers
app.include_router(user_router)
