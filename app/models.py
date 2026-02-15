from sqlalchemy import Column , Integer ,String , ForeignKey

from sqlalchemy.orm import relationship

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String,unique=True)
    phone = Column(String)
    role = Column(String)

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer,primary_key=True ,index=True)
    title = Column(String)
    organizer_id = Column(Integer,ForeignKey("users.id"))
    venue = Column(String)
    start_time = Column(Integer)
    end_time = Column(Integer)
    total_tickets = Column(Integer)
    available_tickets = Column(Integer)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer,primary_key=True)
    event_id = Column(Integer,ForeignKey("events.id"))
    user_id = Column(Integer,ForeignKey("users.id"))