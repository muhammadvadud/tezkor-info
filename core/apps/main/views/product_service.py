from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from core.apps.main.models import ProductServiceModel
from core.apps.main.serializers.product_service import (
    CreateProductServiceSerializer,
    ListProductServiceSerializer,
    RetrieveProductServiceSerializer,
)


@extend_schema(tags=["ProductService"])
class ProductServiceView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = ProductServiceModel.objects.all()
    serializer_class = ListProductServiceSerializer
    permission_classes = [AllowAny]

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductServiceSerializer,
        "retrieve": RetrieveProductServiceSerializer,
        "create": CreateProductServiceSerializer,
    }
