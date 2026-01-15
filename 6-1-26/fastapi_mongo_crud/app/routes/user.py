from fastapi import APIRouter, HTTPException
from app.schemas.user import UserCreate, UserUpdate
from app.crud.user import create_user, get_all_users, get_user, update_user, delete_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("")
async def add_user(user: UserCreate):
    return await create_user(user.dict())

@router.get("")
async def list_users():
    return await get_all_users()

@router.get("/{id}")
async def get_single_user(id: str):
    user = await get_user(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}")
async def update_single_user(id: str, user: UserUpdate):
    updated = await update_user(id, user.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@router.delete("/{id}")
async def delete_single_user(id: str):
    deleted = await delete_user(id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
