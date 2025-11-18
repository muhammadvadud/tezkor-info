from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.payme import PaymeCallBackAPIView

router = DefaultRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("payme/update/", PaymeCallBackAPIView.as_view(), name="payme_callback"),
]
