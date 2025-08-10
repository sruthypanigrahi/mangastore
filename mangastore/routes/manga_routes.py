# from fastapi import APIRouter, HTTPException, Depends
# from app.schemas import MangaCreate, Manga
# from app.database import manga_collection, object_id_to_str
# from typing import List

# router = APIRouter()

# @router.post("/", response_model=Manga)
# async def create_manga(manga: MangaCreate):
#     manga_dict = manga.dict()
#     result = await manga_collection.insert_one(manga_dict)
#     manga_dict["id"] = str(result.inserted_id)
#     return manga_dict

# @router.get("/", response_model=List[Manga])
# async def list_mangas():
#     mangas_cursor = manga_collection.find()
#     mangas = []
#     async for manga in mangas_cursor:
#         mangas.append(object_id_to_str(manga))
#     return mangas

# @router.get("/{manga_id}", response_model=Manga)
# async def get_manga(manga_id: str):
#     manga = await manga_collection.find_one({"_id": ObjectId(manga_id)})
#     if not manga:
#         raise HTTPException(status_code=404, detail="Manga not found")
#     return object_id_to_str(manga)
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.schemas import MangaCreate, Manga
from app.database import manga_collection, object_id_to_str
from typing import List
from bson import ObjectId
import pandas as pd
import tempfile
import ast

router = APIRouter()

# ----------------- Existing Routes -----------------
@router.post("/", response_model=Manga)
async def create_manga(manga: MangaCreate):
    manga_dict = manga.dict()
    result = await manga_collection.insert_one(manga_dict)
    manga_dict["id"] = str(result.inserted_id)
    return manga_dict

@router.get("/", response_model=List[Manga])
async def list_mangas():
    mangas_cursor = manga_collection.find()
    mangas = []
    async for manga in mangas_cursor:
        mangas.append(object_id_to_str(manga))
    return mangas

@router.get("/{manga_id}", response_model=Manga)
async def get_manga(manga_id: str):
    manga = await manga_collection.find_one({"_id": ObjectId(manga_id)})
    if not manga:
        raise HTTPException(status_code=404, detail="Manga not found")
    return object_id_to_str(manga)

# ----------------- New Routes -----------------
@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Invalid file format. Upload an Excel file.")

    # Save uploaded file temporarily
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(await file.read())
    temp_file.close()

    df = pd.read_excel(temp_file.name)

    # Helper functions for parsing
    def parse_int(value):
        if pd.isna(value):
            return None
        return int(str(value).replace(",", "").strip())

    def parse_list(value):
        try:
            return ast.literal_eval(value) if isinstance(value, str) else []
        except:
            return []

    # Clean fields
    if "Members" in df.columns:
        df["Members"] = df["Members"].apply(parse_int)
    if "Favorite" in df.columns:
        df["Favorite"] = df["Favorite"].apply(parse_int)
    if "Popularity" in df.columns:
        df["Popularity"] = df["Popularity"].apply(parse_int)
    if "Genres" in df.columns:
        df["Genres"] = df["Genres"].apply(parse_list)
    if "Themes" in df.columns:
        df["Themes"] = df["Themes"].apply(parse_list)
    if "Demographic" in df.columns:
        df["Demographic"] = df["Demographic"].apply(parse_list)

    records = df.to_dict(orient="records")
    inserted_count = 0
    for record in records:
        result = await manga_collection.update_one(
            {"Title": record["Title"]},
            {"$set": record},
            upsert=True
        )
        if result.upserted_id:
            inserted_count += 1

    return {"inserted": inserted_count, "total_processed": len(records)}

@router.get("/search/by-title/{title}")
async def get_manga_by_title(title: str):
    manga = await manga_collection.find_one({"Title": {"$regex": title, "$options": "i"}})
    if manga:
        return object_id_to_str(manga)
    raise HTTPException(status_code=404, detail="Manga not found")
