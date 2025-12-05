from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivateTypesView,
    AdView,
    CategoryView,
    CompanyLetterSummaryView,
    DashboardAdsView,
    MyadsView,
    PriceCalculationAPIView,
    ProductServiceView,
    ConfirmationAdsView
)

router = DefaultRouter()
router.register("confirmation-ads", ConfirmationAdsView, basename="confirmation-ads")
router.register("dashboard-ads", DashboardAdsView, basename="DashboardAds")
router.register("my-ads", MyadsView, basename="my-ads")
router.register("product-service", ProductServiceView, basename="ProductService")
router.register("category", CategoryView, basename="category")
router.register("ad", AdView, basename="ad")
router.register("activate-types", ActivateTypesView, basename="activate-types")
router.register("company-name-letter", CompanyLetterSummaryView, basename="company-name-letter")
urlpatterns = [
    path("", include(router.urls)),
    path("price-calculation/", PriceCalculationAPIView.as_view(), name="price-calculation"),
]
