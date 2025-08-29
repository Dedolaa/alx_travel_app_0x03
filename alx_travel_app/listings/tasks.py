from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_booking_confirmation_email(booking_id, user_email, listing_title, check_in_date, check_out_date):
    """
    Task to send a booking confirmation email
    """
    subject = f'Booking Confirmation for {listing_title}'
    message = f'''
    Thank you for your booking!
    
    Booking Details:
    - Property: {listing_title}
    - Check-in: {check_in_date}
    - Check-out: {check_out_date}
    - Booking ID: {booking_id}
    
    We look forward to hosting you!
    '''
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        return f"Email sent successfully to {user_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"