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
