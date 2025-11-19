from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymeCallBackAPIView, PaymentsVIew

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("payme/update/", PaymeCallBackAPIView.as_view(), name="payme_callback"),
    path("payments/<str:payment_type>/<int:ad_id>/", PaymentsVIew.as_view(), name="payments"),
]
