from fastapi import APIRouter, HTTPException, Depends, status
from app.schemas import UserCreate, User
from app.database import users_collection, object_id_to_str
from app.auth import get_password_hash, verify_password, create_access_token
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/signup", response_model=User)
async def signup(user: UserCreate):
    existing_user = await users_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    result = await users_collection.insert_one(user_dict)
    user_dict["id"] = str(result.inserted_id)
    user_dict.pop("password")
    return user_dict

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"email": form_data.username})
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user["email"], "role": user["role"], "id": str(user["_id"])})
    return {"access_token": access_token, "token_type": "bearer"}
