from fastapi import APIRouter
from typing import List
from app.services.persistent_db import get_db

router = APIRouter(prefix="/api/admin", tags=["Admin"])

@router.get("/leads")
async def get_leads():
    db = get_db()
    return db["leads"]

@router.get("/metrics")
async def get_metrics():
    db = get_db()
    rooms = db["rooms"]
    bookings = db["bookings"]
    
    total_revenue = sum(b.get("total_price", 0) for b in bookings)
    occupancy_rate = len(bookings) / len(rooms) * 100 if rooms else 0
    
    return {
        "total_revenue": total_revenue,
        "occupancy_rate": f"{occupancy_rate:.1f}%",
        "active_bookings": len(bookings),
        "total_leads": len(db["leads"])
    }
