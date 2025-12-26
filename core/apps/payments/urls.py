from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CashbackView, PaymeCallBackAPIView, PaymentsVIew

router = DefaultRouter()
router.register("cashback", CashbackView, basename="cashback")
urlpatterns = [
    path("", include(router.urls)),
    path("payme/update/", PaymeCallBackAPIView.as_view(), name="payme_callback"),
    path("payments/<str:payment_type>/<int:ad_id>/", PaymentsVIew.as_view(), name="payments"),
]
