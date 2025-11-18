from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivateTypesView,
    AdView,
    CategoryView,
    CompanyLetterSummaryView,
    DashboardAdsView,
    MyadsView,
    PricebracketView,
    PriceCalculationView,
    ProductServiceView,
)

router = DefaultRouter()
router.register("dashboard-ads", DashboardAdsView, basename="DashboardAds")
router.register("my-ads", MyadsView, basename="my-ads")
router.register("product-service", ProductServiceView, basename="ProductService")
router.register("category", CategoryView, basename="category")
router.register("price-bracket", PricebracketView, basename="price-bracket")
router.register("price-calculation", PriceCalculationView, basename="price-calculation")
router.register("ad", AdView, basename="ad")
router.register("activate-types", ActivateTypesView, basename="activate-types")
router.register("company-name-letter", CompanyLetterSummaryView, basename="company-name-letter")
urlpatterns = [path("", include(router.urls))]
