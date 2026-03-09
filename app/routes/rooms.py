from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from app.services.persistent_db import get_db, save_db

router = APIRouter(prefix="/api/rooms", tags=["Rooms"])

class RoomModel(BaseModel):
    id: int
    type: str
    price: float
    features: List[str]
    image_url: str
    available: bool

@router.get("/", response_model=List[RoomModel])
async def get_rooms():
    db = get_db()
    return db["rooms"]

@router.get("/{room_id}", response_model=RoomModel)
async def get_room(room_id: int):
    db = get_db()
    for r in db["rooms"]:
        if r["id"] == room_id:
            return r
    raise HTTPException(status_code=404, detail="Room not found")

@router.post("/check-price")
async def check_dynamic_price(room_id: int, check_in: str):
    """
    Simulates dynamic pricing engine logic.
    For example: Weekends +20%
    """
    db = get_db()
    from datetime import datetime
    room = next((r for r in db["rooms"] if r["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    date_obj = datetime.strptime(check_in, "%Y-%m-%d")
    base_price = room["price"]
    
    # If weekend (Friday = 4, Saturday = 5, Sunday = 6)
    if date_obj.weekday() >= 4:
        # High demand / Weekend
        return {
            "base_price": base_price,
            "dynamic_price": round(base_price * 1.20, 2),
            "reason": "Weekend / High Demand"
        }
        
    return {
        "base_price": base_price,
        "dynamic_price": base_price,
        "reason": "Standard Rate"
    }
