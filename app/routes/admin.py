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

@router.get("/users")
async def get_all_users():
    db = get_db()
    # Strip passwords for admin view
    users = db.get("users", [])
    return [{"id": u["id"], "name": u.get("name"), "email": u.get("email"), "role": u.get("role")} for u in users]

@router.get("/rooms/status")
async def get_rooms_status():
    db = get_db()
    rooms = db.get("rooms", [])
    bookings = db.get("bookings", [])
    
    booked_room_ids = [b["room_id"] for b in bookings if b.get("status") == "Confirmed"]
    
    # Return augmented room data with booked status
    res = []
    for r in rooms:
        res.append({
            "id": r["id"],
            "type": r["type"],
            "price": r["price"],
            "is_booked": r["id"] in booked_room_ids
        })
    return res

@router.get("/ai-operations")
async def get_ai_operations():
    db = get_db()
    
    import random
    from datetime import datetime
    
    # Mocked AI logic based on DB state
    bookings = db.get("bookings", [])
    booked_count = sum(1 for b in bookings if b.get("status") == "Confirmed")
    
    current_time = datetime.now().strftime("%I:%M %p")
    
    return {
        "housekeeping": [
            {
                "room_id": random.choice([2, 10, 24]), 
                "priority": "High", 
                "time_predicted": "09:30 AM",
                "assignee": "Maria G.",
                "reason": "Checkout confirmed. Next guest arrives at 2:00 PM. Requires fast turnaround."
            },
            {
                "room_id": random.choice([5, 12, 18]), 
                "priority": "Medium", 
                "time_predicted": "11:00 AM",
                "assignee": "Julia S.",
                "reason": "Stayover. Guest requested extra towels via app."
            },
            {
                "room_id": random.choice([14, 45, 50]), 
                "priority": "Low", 
                "time_predicted": "02:15 PM",
                "assignee": "Pending",
                "reason": "Routine deep clean. No immediate occupancy."
            }
        ],
        "maintenance": [
            {
                "equipment": f"Room {random.randint(20, 40)} HVAC Unit", 
                "status": "Warning", 
                "probability": "85%",
                "prediction": "Abnormal compressor power draw. Likely to fail in 48-72 hours. Recommended action: Inspect capacitor."
            },
            {
                "equipment": "Main Boiler System", 
                "status": "Critical", 
                "probability": "98%",
                "prediction": "Pressure dropping consistently by 0.5 psi/hr. Immediate inspection required to avoid hot water outage."
            },
            {
                "equipment": "Elevator B", 
                "status": "Routine", 
                "probability": "12%",
                "prediction": "Nearing 5,000 cycle threshold. Schedule regular maintenance within next 2 weeks."
            }
        ],
        "staffing": {
            "prediction": f"High booking volume detected ({booked_count} active reservations this weekend). Expected 95% occupancy.",
            "recommendation": "Maintain full front-desk staff. Schedule 4 additional housekeeping shifts and 1 extra bellhop for the weekend surge.",
            "efficiency_gain": "+28%",
            "cost_savings": "₹12,500/week"
        }
    }
