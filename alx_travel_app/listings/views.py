from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer
from rest_framework import request
from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Payment
from .tasks import send_booking_confirmation_email  


class ListingViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
def index(request):
    return HttpResponse("Hello from listings app!")


class InitiatePaymentView(APIView):
    def post(self, request):
        booking_reference = request.data.get("booking_reference")
        amount = request.data.get("amount")
        email = request.data.get("email")

        payload = {
            "amount": amount,
            "currency": "ETB",  # Or NGN if supported
            "email": email,
            "tx_ref": booking_reference,
            "callback_url": "http://localhost:8000/api/payments/verify/",
            "return_url": "http://localhost:8000/payment-success/"
        }

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        response = request.post(f"{settings.CHAPA_BASE_URL}/transaction/initialize", json=payload, headers=headers)
        data = response.json()

        if response.status_code == 200 and data.get("status") == "success":
            transaction_id = data["data"]["tx_ref"]
            Payment.objects.create(
                booking_reference=booking_reference,
                amount=amount,
                status="Pending",
                transaction_id=transaction_id
            )
            return Response({"payment_url": data["data"]["checkout_url"]})
        return Response(data, status=400)

class VerifyPaymentView(APIView):
    def get(self, request):
        tx_ref = request.query_params.get("tx_ref")

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }
        response = request.get(f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}", headers=headers)
        data = response.json()

        try:
            payment = Payment.objects.get(transaction_id=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=404)

        if data.get("status") == "success" and data["data"]["status"] == "success":
            payment.status = "Completed"
        else:
            payment.status = "Failed"
        payment.save()

        return Response({"payment_status": payment.status})


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Get the booking instance
        booking = serializer.instance
        
        # Trigger the email task asynchronously
        send_booking_confirmation_email.delay(
            booking_id=booking.id,
            user_email=booking.user.email,
            listing_title=booking.listing.title,
            check_in_date=booking.check_in_date.strftime('%Y-%m-%d'),
            check_out_date=booking.check_out_date.strftime('%Y-%m-%d')
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)