from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import ActivateTypesView, AdView, CompanyLetterSummaryView, PricebracketView, PriceCalculationView

router = DefaultRouter()
router.register("price-bracket", PricebracketView, basename="price-bracket")
router.register("price-calculation", PriceCalculationView, basename="price-calculation")
router.register("ad", AdView, basename="ad")
router.register("activate-types", ActivateTypesView, basename="activate-types")
router.register("company-name-letter", CompanyLetterSummaryView, basename="company-name-letter")
urlpatterns = [path("", include(router.urls))]
