# ALX Travel App 0x02 — Chapa API Payment Integration

## 📌 Project Overview
This project extends the functionality of `alx_travel_app_0x01` by integrating **Chapa API** to handle secure online payments for bookings.  
It allows users to:
- Initiate payments
- Redirect to Chapa checkout
- Verify payment status
- Update payment records in the database
- Handle failed payments gracefully

---

## 🚀 Features
- **Payment Initiation**: Creates a Chapa transaction and returns a checkout link.
- **Payment Verification**: Confirms payment status from Chapa and updates the database.
- **Booking Workflow Integration**: Initiates payment after booking creation.
- **Status Tracking**: Payment records stored in the `Payment` model.
- **Sandbox Testing**: Fully functional with Chapa sandbox environment.
- **Secure Credentials**: API keys stored in `.env` file.

---

## 🛠️ Tech Stack
- Python 3.10+
- Django 4.x
- Django REST Framework
- Chapa API
- Requests library
- python-dotenv for environment variables

---

## 📂 Project Structure


# ✈️ ALX Travel App - Background Email with Celery + RabbitMQ

## Overview
This project demonstrates how to configure **Celery with RabbitMQ** to handle background tasks.  
We implement an **email notification system** that sends booking confirmations asynchronously.

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt

# Run RabbitMQ
docker run -d --hostname my-rabbit --name some-rabbit -p 5672:5672 rabbitmq:3

# Run Django migrations
python manage.py migrate

# Start services
#Django server:
python manage.py runserver

# Celery worker:
celery -A alx_travel_app worker -l info