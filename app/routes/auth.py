from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.persistent_db import get_db, save_db

router = APIRouter(prefix="/api/auth", tags=["Auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str
    email: str
    password: str

class UserUpdateRequest(BaseModel):
    name: str
    email: str

@router.post("/login")
async def login(req: LoginRequest):
    db = get_db()
    users = db["users"]
    user = next((u for u in users if u["email"] == req.email and u["password"] == req.password), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        },
        "token": "fake-jwt-token-123"
    }

@router.post("/signup")
async def signup(req: SignupRequest):
    db = get_db()
    users = db["users"]
    if any(u["email"] == req.email for u in users):
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_user = {
        "id": len(users) + 1,
        "name": req.name,
        "email": req.email,
        "password": req.password,
        "role": "guest"
    }
    users.append(new_user)
    save_db()
    
    return {
        "message": "Signup successful",
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"]
        },
        "token": "fake-jwt-token-123"
    }

@router.put("/user/{user_id}")
async def update_user(user_id: str, req: UserUpdateRequest):
    db = get_db()
    users = db["users"]
    for user in users:
        if str(user["id"]) == user_id:
            user["name"] = req.name
            user["email"] = req.email
            save_db()
            return {"message": "Profile updated", "user": {"id": user["id"], "name": user["name"], "email": user["email"], "role": user.get("role", "guest")}}
            
    raise HTTPException(status_code=404, detail="User not found")
