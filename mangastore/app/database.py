# from motor.motor_asyncio import AsyncIOMotorClient
# from bson.objectid import ObjectId

# MONGO_DETAILS = "mongodb://localhost:27017"

# client = AsyncIOMotorClient(MONGO_DETAILS)
# database = client.manga_store

# manga_collection = database.get_collection("mangas")
# users_collection = database.get_collection("users")
# orders_collection = database.get_collection("orders")

# def object_id_to_str(obj):
#     obj["_id"] = str(obj["_id"])
#     return obj
# app/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from environment variable
MONGO_DETAILS = os.getenv("MONGODB_URI")

# Create client connection
client = AsyncIOMotorClient(MONGO_DETAILS)

# Select database
database = client.manga_store

# Collections
manga_collection = database.get_collection("mangas")
users_collection = database.get_collection("users")
orders_collection = database.get_collection("orders")

# Helper to convert ObjectId to string
def object_id_to_str(obj):
    obj["_id"] = str(obj["_id"])
    return obj
