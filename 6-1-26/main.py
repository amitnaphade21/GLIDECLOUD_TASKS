from fastapi import FastAPI, HTTPException
from schemas import UserCreate, UserUpdate
from crud import create_user, get_all_users, get_user, update_user, delete_user

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI Mongo CRUD Running"}

@app.post("/users")
async def add_user(user: UserCreate):
    return await create_user(user.dict())

@app.get("/users")
async def list_users():
    return await get_all_users()

@app.get("/users/{id}")
async def get_single_user(id: str):
    user = await get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{id}")
async def update_single_user(id: str, user: UserUpdate):
    updated = await update_user(id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{id}")
async def delete_single_user(id: str):
    deleted = await delete_user(id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
