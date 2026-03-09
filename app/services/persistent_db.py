import json
import os
from datetime import datetime, timedelta

DB_FILE = os.path.join(os.path.dirname(__file__), "database.json")

# Initial Seeding Data with far more real-time hotel vibes
INITIAL_DATA = {
    "users": [
        {
            "id": 1,
            "name": "Sai Kiran",
            "email": "sai@example.com",
            "password": "password123", # Only used as a mock fallback if Supabase unavailable
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
            "price": 120,
            "features": ["Queen Bed", "Free WiFi", "Smart TV", "City View"],
            "image_url": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 2,
            "type": "Deluxe Room",
            "price": 180,
            "features": ["King Bed", "Ocean View", "Mini Bar", "Balcony", "Free WiFi"],
            "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 3,
            "type": "Executive Suite",
            "price": 350,
            "features": ["King Bed", "Living Room", "Jacuzzi", "Panoramic Ocean View", "Personal Butler"],
            "image_url": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 4,
            "type": "Family Suite",
            "price": 280,
            "features": ["2 King Beds", "Kitchenette", "Living Area", "Kids Play Area", "Free WiFi"],
            "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 5,
            "type": "Penthouse",
            "price": 850,
            "features": ["Private Pool", "3 Bedrooms", "Private Chef", "Helicopter Transfer", "Spa Access"],
            "image_url": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&q=80&w=800",
            "available": True
        },
        {
            "id": 6,
            "type": "Cozy Single",
            "price": 80,
            "features": ["Single Bed", "Work Desk", "Free WiFi", "City View", "Espresso Machine"],
            "image_url": "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?auto=format&fit=crop&q=80&w=800",
            "available": False
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
            "special_request": "Extra pillows, quiet room requested.",
            "total_price": 540,
            "status": "Confirmed",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ],
    "guest_preferences": [
        {
            "user_id": 1,
            "preferred_room": "Deluxe Room",
            "food_preference": "Vegan / Plant-based",
            "temperature_preference": "20°C / 68°F",
            "previous_stays": 4
        }
    ],
    "leads": [
        {
            "id": 1,
            "name": "Jane Smith",
            "email": "jane@example.com",
            "interaction_type": "Chatbot Pricing Inquiry",
            "status": "Contacted"
        },
        {
            "id": 2,
            "name": "Mark Johnson",
            "email": "mark.j@example.com",
            "interaction_type": "Abondoned Booking (Penthouse)",
            "status": "Pending"
        }
    ],
    "ai_insights": {
        "predicted_busy_days": ["Friday", "Saturday", "Upcoming Holiday Week"],
        "cleaning_schedule": "Priority Focus: Penthouse, 3 Deluxe Rooms requiring deep clean post-checkout.",
        "staff_workload": "Surge expected this weekend. Recommending scheduling 3 extra housekeepers and 1 extra valet."
    }
}

class PersistentDB:
    def __init__(self):
        self.data_store = INITIAL_DATA.copy()
        self.load()

    def load(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, "r") as f:
                    file_data = json.load(f)
                    # Merge only missing keys or update everything
                    self.data_store.update(file_data)
            except Exception as e:
                print(f"Error loading DB: {e}. Using initial data.")
                self.save()
        else:
            self.save()

    def save(self):
        with open(DB_FILE, "w") as f:
            json.dump(self.data_store, f, indent=4)

    def get_data(self):
        self.load()
        return self.data_store

db_instance = PersistentDB()

def get_db():
    return db_instance.get_data()

def save_db():
    db_instance.save()
