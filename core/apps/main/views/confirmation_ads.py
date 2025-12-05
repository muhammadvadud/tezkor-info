from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.apps.accounts.choices.user import RoleChoice
from core.apps.main.models import AdModel
from core.apps.main.serializers.confirmation_ads import (
    UpdateConfirmationAdsSerializer,
    ListConfirmationAdsSerializer,
    RetrieveConfirmationAdsSerializer,
)


@extend_schema(tags=["Confirmation Ads"])
class ConfirmationAdsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = AdModel.objects.filter(status="PAID")
    serializer_class = ListConfirmationAdsSerializer
    permission_classes = [IsAdminUser]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListConfirmationAdsSerializer,
        "retrieve": RetrieveConfirmationAdsSerializer,
        "partial_update": UpdateConfirmationAdsSerializer,
    }
