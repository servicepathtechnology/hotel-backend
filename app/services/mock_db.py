import json
from datetime import datetime, timedelta

# Mock Database Store (In-Memory for Demo Purposes)

mock_db = {
    "users": [
        {
            "id": 1,
            "name": "Sai Kiran",
            "email": "sai@example.com",
            "password": "password123", # Mock demo password
            "role": "guest"
        },
        {
            "id": 2,
            "name": "Admin User",
            "email": "admin@hotel.com",
            "password": "admin",
            "role": "admin"
        }
    ],
    "rooms": [
        {
            "id": 1,
            "type": "Standard Room",
            "price": 100,
            "features": ["Queen Bed", "Free WiFi", "TV", "City View"],
            "image_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 2,
            "type": "Deluxe Room",
            "price": 150,
            "features": ["King Bed", "Ocean View", "Mini Bar", "Balcony", "Free WiFi"],
            "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 3,
            "type": "Suite Room",
            "price": 250,
            "features": ["King Bed", "Living Room", "Jacuzzi", "Ocean View", "Butler Service"],
            "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&q=80&w=800",
            "available": True
        }
    ],
    "bookings": [
        {
            "id": 1,
            "user_id": 1,
            "room_id": 2,
            "check_in": (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d"),
            "check_out": (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d"),
            "guests": 2,
            "special_request": "Extra pillows please",
            "total_price": 450,
            "status": "Confirmed",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ],
    "guest_preferences": [
        {
            "user_id": 1,
            "preferred_room": "Deluxe Room",
            "food_preference": "Vegetarian",
            "temperature_preference": "22°C",
            "previous_stays": 2
        }
    ],
    "leads": [
        {
            "id": 1,
            "name": "Ali",
            "email": "ali@example.com",
            "interaction_type": "Chatbot Request",
            "status": "Pending"
        }
    ],
    "ai_insights": {
        "predicted_busy_days": ["Friday", "Saturday"],
        "cleaning_schedule": "Priority: Rooms 101, 102 (Check-outs today)",
        "staff_workload": "High demand expected this weekend. Suggest +2 Housekeeping staff."
    }
}

def get_db():
    return mock_db
