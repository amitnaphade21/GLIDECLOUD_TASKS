from database import collection
from bson import ObjectId
from models import user_helper

async def create_user(user_data: dict):
    user = await collection.insert_one(user_data)
    new_user = await collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

async def get_all_users():
    users = []
    async for user in collection.find():
        users.append(user_helper(user))
    return users

async def get_user(id: str):
    user = await collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    await collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    user = await collection.find_one({"_id": ObjectId(id)})
    return user_helper(user)

async def delete_user(id: str):
    result = await collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count