from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.accounts.models import Country
from core.apps.main.serializers.countries import (
    CreateCountriesSerializer,
    ListCountriesSerializer,
    RetrieveCountriesSerializer,
)


@extend_schema(tags=["Countries"])
class CountriesView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = Country.objects.prefetch_related(
        'region__districts'
    )

    serializer_class = ListCountriesSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCountriesSerializer,
        "retrieve": RetrieveCountriesSerializer,
        "create": CreateCountriesSerializer,
    }
