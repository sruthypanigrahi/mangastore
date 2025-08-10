from fastapi import APIRouter, HTTPException, status
from typing import List
from app.schemas import Order, OrderCreate
from app.database import orders_collection, object_id_to_str
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate):
    order_dict = order.dict()
    result = await orders_collection.insert_one(order_dict)
    order_dict["id"] = str(result.inserted_id)
    return order_dict

@router.get("/", response_model=List[Order])
async def list_orders():
    orders_cursor = orders_collection.find()
    orders = []
    async for order in orders_cursor:
        orders.append(object_id_to_str(order))
    return orders

@router.get("/{order_id}", response_model=Order)
async def get_order(order_id: str):
    order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return object_id_to_str(order)

@router.put("/{order_id}", response_model=Order)
async def update_order_status(order_id: str, status: str):
    result = await orders_collection.update_one({"_id": ObjectId(order_id)}, {"$set": {"status": status}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    updated_order = await orders_collection.find_one({"_id": ObjectId(order_id)})
    return object_id_to_str(updated_order)
