from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from core.apps.main.filters import CategoryFilter
from core.apps.main.models import CategoryModel
from core.apps.main.serializers.category import (
    CreateCategorySerializer,
    ListCategorySerializer,
    RetrieveCategorySerializer,
    ListCategoryTreeSerializer,
)


@extend_schema(tags=["category"])
class CategoryView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = ListCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    action_permission_classes = {}
    action_serializer_class = {
        "list": ListCategorySerializer,
        "retrieve": RetrieveCategorySerializer,
        "create": CreateCategorySerializer,
    }

    def get_queryset(self):
        parent_id = self.request.query_params.get("parent")

        if parent_id:
            return CategoryModel.objects.filter(parent_id=parent_id).order_by("order", "id")
        return CategoryModel.objects.filter(level=2).order_by("order", "id")

    def get_serializer_class(self):
        is_tree = self.request.query_params.get('is_tree', '').lower() == 'true'
        if is_tree:
            return ListCategoryTreeSerializer

        return super().get_serializer_class()
