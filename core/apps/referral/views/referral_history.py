from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.referral.models import ReferralHistoryModel
from core.apps.referral.serializers.referral_history import (
    CreateReferralHistorySerializer,
    ListReferralHistorySerializer,
    RetrieveReferralHistorySerializer,
)


@extend_schema(tags=["ReferralHistory"])
class ReferralHistoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ReferralHistoryModel.objects.all()
    serializer_class = ListReferralHistorySerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListReferralHistorySerializer,
        "retrieve": RetrieveReferralHistorySerializer,
        "create": CreateReferralHistorySerializer,
    }
