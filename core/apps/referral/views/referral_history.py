from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from core.apps.referral.filters import ReferralHistoryFilter
from core.apps.referral.permissions import ReferralPermission
from core.apps.referral.models import ReferralHistoryModel
from core.apps.referral.serializers.referral_history import (
    CreateReferralHistorySerializer,
    ListReferralHistorySerializer,
    RetrieveReferralHistorySerializer,
)


@extend_schema(tags=["ReferralHistory"])
class ReferralHistoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ReferralHistoryModel.objects.all().order_by("-id")
    serializer_class = ListReferralHistorySerializer
    permission_classes = [ReferralPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReferralHistoryFilter

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListReferralHistorySerializer,
        "retrieve": RetrieveReferralHistorySerializer,
        "create": CreateReferralHistorySerializer,
    }
