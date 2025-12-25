from django_filters import rest_framework as filters
from core.apps.main.models import LegalDocumentsModels


class LegalDocumentsFilter(filters.FilterSet):
    class Meta:
        model = LegalDocumentsModels
        fields = [
            "type"
        ]
