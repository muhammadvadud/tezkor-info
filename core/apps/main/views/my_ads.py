from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.apps.main.models import AdModel
from core.apps.accounts.choices.user import PersonTypeChoice
from core.apps.main.serializers.my_ads import CreateMyadsSerializer, ListMyadsSerializer, RetrieveMyadsSerializer


@extend_schema(tags=["MyAds"])
class MyadsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = AdModel.objects.all()
    serializer_class = ListMyadsSerializer
    permission_classes = [IsAuthenticated]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListMyadsSerializer,
        "retrieve": RetrieveMyadsSerializer,
        "create": CreateMyadsSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if user.person_type == PersonTypeChoice.LEGAL_ENTITY:
            return AdModel.objects.filter(created_by=user).order_by("-id")
        if user.person_type == PersonTypeChoice.EMPLOYEE and user.parent:
            return AdModel.objects.filter(created_by=user.parent).order_by("-id")
        return AdModel.objects.none()
