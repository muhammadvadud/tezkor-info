from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema

from ..filters import ProductServiceFilter
from ..permissions.product_service import ProductServicePermission
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from core.apps.main.models import ProductServiceModel
from core.apps.accounts.models.region import Country
from django.db.models import Q
from core.apps.main.serializers.product_service import (
    CreateProductServiceSerializer,
    ListProductServiceSerializer,
    RetrieveProductServiceSerializer,
    GetLegalEntitySerializer,
    GetCountrySerializer,
)


@extend_schema(tags=["ProductService"])
class ProductServiceView(BaseViewSetMixin, ModelViewSet):
    queryset = ProductServiceModel.objects.all()
    serializer_class = ListProductServiceSerializer
    permission_classes = [ProductServicePermission]
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filter_class = ProductServiceFilter
    search_fields = ["title", "description", "company__company_name", "category__name"]
    action_permission_classes = {}
    action_serializer_class = {
        "list": ListProductServiceSerializer,
        "retrieve": RetrieveProductServiceSerializer,
        "partial_update": CreateProductServiceSerializer,
        "create": CreateProductServiceSerializer,
    }

    @action(detail=False, methods=["get"], url_path="product-service-legal-entity")
    def get_legal_entity(self, request):
        queryset = get_user_model().objects.filter(
            person_type="legal_entity",
            validated_at__isnull=False
        )
        search = request.query_params.get("search")

        if search:
            queryset = queryset.filter(
                Q(company_name__icontains=search) |
                Q(product_service_company__title__icontains=search) |
                Q(product_service_company__description__icontains=search) |
                Q(product_service_company__category__name__icontains=search)
            ).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetLegalEntitySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetLegalEntitySerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="product-service-country")
    def get_country(self, request):
        queryset = Country.objects.all()
        search = request.query_params.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(region__districts__user__company_name__icontains=search) |
                Q(region__districts__user__product_service_company__title__icontains=search) |
                Q(region__districts__user__product_service_company__description__icontains=search) |
                Q(region__districts__user__product_service_company__category__name__icontains=search)
            ).distinct()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = GetCountrySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = GetCountrySerializer(queryset, many=True)
        return Response(serializer.data)
