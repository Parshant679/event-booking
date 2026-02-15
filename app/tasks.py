from app.worker import celery

@celery.task
def send_booking_confirmations(booking_id):
    print(f"Sending comfirmation for booking {booking_id}")

@celery.task
def notify_event_updates(event_id):
    print(f"Sending updates for event {event_id}")