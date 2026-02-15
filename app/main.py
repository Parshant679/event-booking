from fastapi import FastAPI , Depends ,HTTPException

from sqlalchemy.orm import Session
from .database import Base,engine,SessionLocal

from . import models , schemas

from .tasks import send_booking_confirmations ,notify_event_updates

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close


@app.post("/users")
def create_user(user: schemas.UserCreate ,db: Session = Depends(get_db)):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/events/{organizer_id}")
def create_event(organizer_id:int,event: schemas.EventCreate ,db: Session = Depends(get_db)):
   user = db.query(models.User).filter(models.User.id == organizer_id).first()
   if not user or user.role != "organizer":
       raise HTTPException(status_code=403 ,detail="Only organizers can create events")
   db_event = models.Event(**event.model_dump())
   db.add(db_event)
   db.commit()
   db.refresh(db_event) 

from sqlalchemy import text

@app.post("/book/{user_id}")
def book_ticket(user_id: int, booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user or user.role != "customer":
        raise HTTPException(status_code=403, detail="Only customers can book")
    result = db.execute(
        text("""
            UPDATE events
            SET available_tickets = available_tickets - 1
            WHERE id = :event_id AND available_tickets > 0
            RETURNING id
        """),
        {"event_id": booking.event_id}
    )
    updated_event = result.fetchone()
    if not updated_event:
        raise HTTPException(status_code=400, detail="No tickets available")
    db_booking = models.Booking(
        event_id=booking.event_id,
        user_id=user_id
    )

    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    send_booking_confirmations.delay(db_booking.id)

    return db_booking

@app.put("/events/{event_id}")
def update_event(event_id:int ,event:schemas.EventCreate ,db:Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == event_id).first()
    if not user or user.role != "organizer":
        raise HTTPException(status_code=403 ,detail="Only customers can update events")
    if event.start_time > event.end_time:
        raise HTTPException(status_code=400 ,detail="Start time cannot be greater than end time")
    db_event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not db_event:
        raise HTTPException(status_code=404 ,detail="Event not found")
    db_event.title = event.title
    db_event.venue = event.venue
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db.commit()
    db.refresh(db_event)

    notify_event_updates.delay(db_event.id)

    return db_event
