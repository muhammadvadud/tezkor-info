from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from core.apps.main.choices.payment_status import PaymentsStatusChoice
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins
from core.apps.main.models import AdModel
from core.apps.main.permissions import ConfirmationAdsPermission
from core.apps.main.serializers.confirmation_ads import (
    UpdateConfirmationAdsSerializer,
    ListConfirmationAdsSerializer,
    RetrieveConfirmationAdsSerializer,
)


@extend_schema(tags=["Confirmation Ads"])
class ConfirmationAdsView(BaseViewSetMixin, ModelViewSet):
    queryset = AdModel.objects.filter(status=PaymentsStatusChoice.PAID)
    serializer_class = ListConfirmationAdsSerializer
    permission_classes = [ConfirmationAdsPermission]
    http_method_names = ["get", "patch", "head", "options"]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListConfirmationAdsSerializer,
        "retrieve": RetrieveConfirmationAdsSerializer,
        "partial_update": UpdateConfirmationAdsSerializer,
    }
