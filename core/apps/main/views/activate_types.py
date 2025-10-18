from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.main.models import ActivateTypesModel
from core.apps.main.serializers.activate_types.activate_types import (
    CreateActivateTypesSerializer,
    ListActivateTypesSerializer,
    RetrieveActivateTypesSerializer,
)


@extend_schema(tags=["ActivateTypes"])
class ActivateTypesView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ActivateTypesModel.objects.all()
    serializer_class = ListActivateTypesSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListActivateTypesSerializer,
        "retrieve": RetrieveActivateTypesSerializer,
        "create": CreateActivateTypesSerializer,
    }
