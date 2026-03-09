from fastapi import APIRouter
from app.services.persistent_db import get_db, save_db

router = APIRouter(prefix="/api/ai", tags=["AI"])

@router.post("/chat")
async def chat_interaction(message: str):
    """
    Simulated AI Chatbot processing.
    Detects basic intents and replies accordingly.
    """
    db = get_db()
    msg = message.lower()
    
    # Save lead interaction
    db["leads"].append({
        "id": len(db["leads"]) + 1,
        "name": "Guest",
        "email": "Pending",
        "interaction_type": "Chatbot",
        "status": "Pending"
    })
    save_db()
    
    intent = "general_query"
    if "book" in msg or "room" in msg:
        intent = "booking"
        return {"response": "I'd be happy to help you find a room! What dates are you looking to stay with us?", "intent": intent}
    elif "price" in msg or "cost" in msg:
        intent = "pricing"
        return {"response": "Our rooms range from $100 for Standard to $250 for Suites. Our AI pricing ensures the best rate based on demand.", "intent": intent}
    else:
        return {"response": "I'm the AI Hotel Assistant. I can help you book rooms, check availability, or manage your stay. How can I assist you today?", "intent": intent}

@router.get("/recommendations/{user_id}")
async def get_recommendations(user_id: str):
    db = get_db()
    prefs = next((p for p in db["guest_preferences"] if str(p["user_id"]) == str(user_id)), None)
    if not prefs:
        return {"recommended_room": "Deluxe Room", "food": "Chef's Special", "offers": ["10% off SPA"]}
        
    return {
        "recommended_room": prefs["preferred_room"],
        "food": prefs["food_preference"],
        "offers": [f"Welcome back! Enjoy a complimentary {prefs['food_preference']} breakfast on us."]
    }

@router.get("/insights")
async def get_insights():
    db = get_db()
    return db["ai_insights"]
