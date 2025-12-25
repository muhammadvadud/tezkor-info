from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from core.apps.referral.permissions import ReferralPermission
from rest_framework.viewsets import ModelViewSet
from core.apps.accounts.choices.user import PersonTypeChoice
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
    permission_classes = [ReferralPermission]
    http_method_names = ["get", "post", "head", "options"]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListReferralSerializer,
        "retrieve": RetrieveReferralSerializer,
        "create": CreateReferralSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if user.person_type == PersonTypeChoice.LEGAL_ENTITY:
            return ReferralModel.objects.filter(user=self.request.user)
        elif user.person_type == PersonTypeChoice.EMPLOYEE:
            return ReferralModel.objects.filter(user=self.request.user.parent)
        return ReferralModel.objects.none()
