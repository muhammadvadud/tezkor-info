from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from core.apps.main.permissions import AdPermission
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.exceptions import ValidationError
from core.apps.main.models import AdModel
from core.apps.main.serializers.my_ads import CreateMyadsSerializer, ListMyadsSerializer, RetrieveMyadsSerializer


@extend_schema(tags=["MyAds"])
class MyadsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = AdModel.objects.all()
    serializer_class = ListMyadsSerializer
    permission_classes = [AdPermission]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListMyadsSerializer,
        "retrieve": RetrieveMyadsSerializer,
        "create": CreateMyadsSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            raise ValidationError("You must be logged in to view this page.")
        return AdModel.objects.filter(created_by=user).order_by("-id")
