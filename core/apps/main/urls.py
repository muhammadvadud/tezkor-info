from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    ActivateTypesView,
    AdView,
    CategoryView,
    CompanyLetterSummaryView,
    PricebracketView,
    PriceCalculationView,
)

router = DefaultRouter()
router.register("category", CategoryView, basename="category")
router.register("price-bracket", PricebracketView, basename="price-bracket")
router.register("price-calculation", PriceCalculationView, basename="price-calculation")
router.register("ad", AdView, basename="ad")
router.register("activate-types", ActivateTypesView, basename="activate-types")
router.register("company-name-letter", CompanyLetterSummaryView, basename="company-name-letter")
urlpatterns = [path("", include(router.urls))]
