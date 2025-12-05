from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from core.apps.main.filters.business_about import BusinessAboutFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from core.apps.main.serializers.business_about import (
    CreateBusinessAboutSerializer,
    ListBusinessAboutSerializer,
    RetrieveBusinessAboutSerializer,
)


@extend_schema(tags=["BusinessAbout"])
class BusinessAboutView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = ListBusinessAboutSerializer
    permission_classes = [AllowAny]
    filterset_class = BusinessAboutFilter
    filter_backends = [DjangoFilterBackend]
    action_permission_classes = {}
    action_serializer_class = {
        "list": ListBusinessAboutSerializer,
        "retrieve": RetrieveBusinessAboutSerializer,
        "create": CreateBusinessAboutSerializer,
    }
