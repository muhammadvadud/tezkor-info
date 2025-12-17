from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AdView,
    CategoryView,
    DashboardAdsView,
    MyadsView,
    PriceCalculationAPIView,
    ProductServiceView,
    ConfirmationAdsView,
    BusinessAboutView,
    GetPdfViewSet,
)

router = DefaultRouter()
router.register("ad", GetPdfViewSet, basename="get-pdf")
router.register("business-about", BusinessAboutView, basename="business-about")
router.register("confirmation-ads", ConfirmationAdsView, basename="confirmation-ads")
router.register("dashboard-ads", DashboardAdsView, basename="DashboardAds")
router.register("my-ads", MyadsView, basename="my-ads")
router.register("product-service", ProductServiceView, basename="ProductService")
router.register("category", CategoryView, basename="category")
router.register("ad", AdView, basename="ad")
urlpatterns = [
    path("", include(router.urls)),
    path("price-calculation/", PriceCalculationAPIView.as_view(), name="price-calculation"),
]
