from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from core.apps.main.permissions import EmployeePermission
from django.contrib.auth import get_user_model
from core.apps.main.serializers.add_employee import CreateEmployeeSerializer, ListEmployeeSerializer, \
    RetrieveEmployeeSerializer


@extend_schema(tags=["Employee"])
class EmployeeView(BaseViewSetMixin, ModelViewSet):
    serializer_class = ListEmployeeSerializer
    permission_classes = [EmployeePermission]
    http_method_names = ["get", "post", "head", "options"]
    action_permission_classes = {}
    action_serializer_class = {
        "list": ListEmployeeSerializer,
        "retrieve": RetrieveEmployeeSerializer,
        "create": CreateEmployeeSerializer,
    }

    def get_queryset(self):
        user = self.request.user
        return get_user_model().objects.filter(parent=user).order_by("-id")
