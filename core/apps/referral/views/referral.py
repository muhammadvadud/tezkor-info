from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.referral.models import ReferralModel
from core.apps.referral.serializers.referral import (
    CreateReferralSerializer,
    ListReferralSerializer,
    RetrieveReferralSerializer,
)


@extend_schema(tags=["referral"])
class ReferralView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ReferralModel.objects.all()
    serializer_class = ListReferralSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListReferralSerializer,
        "retrieve": RetrieveReferralSerializer,
        "create": CreateReferralSerializer,
    }
