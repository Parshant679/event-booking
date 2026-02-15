# 🎟 Event Booking System

A role-based event booking system built with:

- FastAPI
- PostgreSQL
- Celery
- Redis
- Docker

This system supports two types of users:

- **Event Organizers** → Create & update events
- **Customers** → Book tickets

Includes background job processing and concurrency-safe ticket booking.

---

# 🏗 Architecture Diagram

                ┌────────────────────┐
                │      Client        │
                │ (Swagger / Postman)│
                └──────────┬─────────┘
                           │
                           ▼
                ┌────────────────────┐
                │      FastAPI       │
                │   (REST API)       │
                └──────────┬─────────┘
                           │
            ┌──────────────┼──────────────┐
            ▼                              ▼
┌────────────────────┐            ┌────────────────────┐
│   PostgreSQL DB    │            │      Redis         │
│ (Users/Events/     │            │   (Message Broker) │
│   Bookings)        │            └──────────┬─────────┘
└────────────────────┘                       │
                                             ▼
                                   ┌────────────────────┐
                                   │     Celery Worker  │
                                   │ Background Tasks   │
                                   └────────────────────┘



# 🚀 Features

## 1️⃣ Role-Based Access

- Organizers can:
  - Create events
  - Update events

- Customers can:
  - Book tickets

---

## 2️⃣ Background Tasks

### 📧 Booking Confirmation
Triggered when a customer books a ticket.

Simulates sending confirmation email using console log.

---

### 🔔 Event Update Notification
Triggered when an organizer updates an event.

Simulates notifying booked users via console log.

---

## 3️⃣ Atomic Ticket Booking

Prevents overselling using atomic SQL:

sql
UPDATE events
SET available_tickets = available_tickets - 1
WHERE id = :event_id AND available_tickets > 0
RETURNING id;

## Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| API              | FastAPI                 |
| Database         | PostgreSQL              |
| ORM              | SQLAlchemy              |
| Background Jobs  | Celery                  |
| Broker           | Redis                   |
| Containerization | Docker + Docker Compose |

## Project Structure
event-booking/
│
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── tasks.py
│   └── worker.py
│
├── requirements.txt
├── Dockerfile
└── docker-compose.yml


