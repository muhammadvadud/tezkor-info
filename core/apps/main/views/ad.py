from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from ..permissions.ad import AdPermission

from core.apps.main.models import AdModel
from core.apps.main.serializers.ad import CreateAdSerializer, ListAdSerializer, RetrieveAdSerializer


@extend_schema(tags=["ad"])
class AdView(BaseViewSetMixin, ModelViewSet):
    queryset = AdModel.objects.all()
    serializer_class = ListAdSerializer
    permission_classes = [AdPermission]
    http_method_names = ["get", "post", "head", "options"]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListAdSerializer,
        "retrieve": RetrieveAdSerializer,
        "create": CreateAdSerializer,
    }
