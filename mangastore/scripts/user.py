from fastapi import APIRouter


router = APIRouter()



@router.get("/users")
async def get_users():
    return {"users": ["user1", "user2", "user3"]}  