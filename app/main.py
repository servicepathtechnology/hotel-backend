from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.auth import router as auth_router
from app.routes.rooms import router as rooms_router
from app.routes.ai import router as ai_router
from app.routes.bookings import router as bookings_router
from app.routes.admin import router as admin_router

app = FastAPI(title="AI Hotel Demo API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        "http://localhost:3000",
        "https://hotel-room-booking-liard.vercel.app"
    ], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(rooms_router)
app.include_router(ai_router)
app.include_router(bookings_router)
app.include_router(admin_router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "AI Hotel Demo API is running. Check /docs for Swagger UI."}
