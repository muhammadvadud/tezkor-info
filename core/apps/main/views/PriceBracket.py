from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.main.models import PriceBracketModel
from core.apps.main.serializers.PriceBracket import (
    CreatePricebracketSerializer,
    ListPricebracketSerializer,
    RetrievePricebracketSerializer,
)


@extend_schema(tags=["PriceBracket"])
class PricebracketView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = PriceBracketModel.objects.all()
    serializer_class = ListPricebracketSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListPricebracketSerializer,
        "retrieve": RetrievePricebracketSerializer,
        "create": CreatePricebracketSerializer,
    }

