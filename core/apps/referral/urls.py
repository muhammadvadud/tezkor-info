from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReferralHistoryView, ReferralView

router = DefaultRouter()
router.register("referral-history", ReferralHistoryView, basename="ReferralHistory")
router.register("referral", ReferralView, basename="referral")
urlpatterns = [path("", include(router.urls))]
