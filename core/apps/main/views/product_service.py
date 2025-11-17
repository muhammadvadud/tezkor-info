from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from ..permissions.product_service import ProductServicePermission
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from core.apps.main.models import ProductServiceModel
from core.apps.main.serializers.product_service import (
    CreateProductServiceSerializer,
    ListProductServiceSerializer,
    RetrieveProductServiceSerializer,
)


@extend_schema(tags=["ProductService"])
class ProductServiceView(BaseViewSetMixin, ModelViewSet):
    queryset = ProductServiceModel.objects.all()
    serializer_class = ListProductServiceSerializer
    permission_classes = [ProductServicePermission]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductServiceSerializer,
        "retrieve": RetrieveProductServiceSerializer,
        "partial_update": CreateProductServiceSerializer,
        "create": CreateProductServiceSerializer,
    }
