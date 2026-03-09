from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)  # Mock representation
    role = Column(String, default="guest")  # admin, guest

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)  # Standard, Deluxe, Suite
    price = Column(Float)
    features = Column(Text)  # JSON-like string or comma separated
    image_url = Column(String)
    available = Column(Boolean, default=True)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    check_in = Column(String)
    check_out = Column(String)
    guests = Column(Integer)
    special_request = Column(Text)
    total_price = Column(Float)
    status = Column(String, default="Confirmed")  # Pending, Confirmed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    interaction_type = Column(String)  # Chatbot, BookingStarted
    status = Column(String, default="Pending")  # Pending, Contacted, Qualified, Booked, Lost
