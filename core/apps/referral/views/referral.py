from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.apps.referral.models import ReferralModel
from core.apps.referral.serializers.referral import (
    CreateReferralSerializer,
    ListReferralSerializer,
    RetrieveReferralSerializer,
)


@extend_schema(tags=["referral"])
class ReferralView(BaseViewSetMixin, ModelViewSet):
    queryset = ReferralModel.objects.all()
    serializer_class = ListReferralSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "head", "options"]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListReferralSerializer,
        "retrieve": RetrieveReferralSerializer,
        "create": CreateReferralSerializer,
    }

    def get_queryset(self):
        return ReferralModel.objects.filter(user=self.request.user)
