from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    role: str

class EventCreate(BaseModel):
    title: str
    organizer_id: int
    venue: str
    start_time: int
    end_time: int
    total_tickets: int
    available_tickets: int

class BookingCreate(BaseModel):
    event_id: int
    user_id: int