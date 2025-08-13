from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet
from . import views
from .views import InitiatePaymentView, VerifyPaymentView

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns = [
    path("payments/initiate/", InitiatePaymentView.as_view(), name="initiate_payment"),
    path("payments/verify/", VerifyPaymentView.as_view(), name="verify_payment"),
]