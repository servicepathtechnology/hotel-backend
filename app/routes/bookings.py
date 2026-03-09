from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime
from app.services.persistent_db import get_db, save_db

router = APIRouter(prefix="/api/bookings", tags=["Bookings"])

class BookingCreate(BaseModel):
    user_id: str
    room_id: int
    check_in: str
    check_out: str
    guests: int
    special_request: str = ""
    total_price: float

@router.get("/", response_model=List[dict])
async def get_all_bookings():
    db = get_db()
    return db["bookings"]

@router.get("/user/{user_id}", response_model=List[dict])
async def get_user_bookings(user_id: str):
    db = get_db()
    return [b for b in db["bookings"] if str(b["user_id"]) == str(user_id)]

@router.post("/")
async def create_booking(req: BookingCreate):
    db = get_db()
    new_booking = {
        "id": len(db["bookings"]) + 1,
        "user_id": req.user_id,
        "room_id": req.room_id,
        "check_in": req.check_in,
        "check_out": req.check_out,
        "guests": req.guests,
        "special_request": req.special_request,
        "total_price": req.total_price,
        "status": "Confirmed",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    db["bookings"].append(new_booking)
    
    # Simulate CRM Auto update
    db["leads"].append({
        "id": len(db["leads"]) + 1,
        "name": f"User {req.user_id}",
        "email": f"user{req.user_id}@demo.com",
        "interaction_type": "Completed Booking",
        "status": "Booked"
    })
    
    save_db()
    return {"message": "Booking confirmed. WhatsApp confirmation sent.", "booking": new_booking}
