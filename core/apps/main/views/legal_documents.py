from django_core.mixins import BaseViewSetMixin
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from core.apps.main.models import LegalDocumentsModels
from core.apps.main.filters.legal_documents import LegalDocumentsFilter
from core.apps.main.serializers.legal_documents import (
    CreateLegalDocumentsSerializer,
    ListLegalDocumentsSerializer,
    RetrieveLegalDocumentsSerializer,
)


@extend_schema(tags=["LegalDocuments"])
class LegalDocumentsView(BaseViewSetMixin, ReadOnlyModelViewSet):
    queryset = LegalDocumentsModels.objects.all()
    serializer_class = ListLegalDocumentsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LegalDocumentsFilter
    permission_classes = [AllowAny]
    action_permission_classes = {}
    action_serializer_class = {
        "list": ListLegalDocumentsSerializer,
        "retrieve": RetrieveLegalDocumentsSerializer,
        "create": CreateLegalDocumentsSerializer,
    }
