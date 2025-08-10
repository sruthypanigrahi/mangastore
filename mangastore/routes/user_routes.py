from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.schemas import User, UserUpdate
from app.database import users_collection, object_id_to_str
from bson.objectid import ObjectId

router = APIRouter()

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return object_id_to_str(user)

@router.get("/", response_model=List[User])
async def list_users():
    users_cursor = users_collection.find()
    users = []
    async for user in users_cursor:
        users.append(object_id_to_str(user))
    return users

@router.put("/{user_id}", response_model=User)
async def update_user(user_id: str, user_update: UserUpdate):
    update_data = {k: v for k, v in user_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No data provided for update")
    result = await users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    return object_id_to_str(updated_user)

@router.delete("/{user_id}")
async def delete_user(user_id: str):
    result = await users_collection.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"detail": "User deleted"}
