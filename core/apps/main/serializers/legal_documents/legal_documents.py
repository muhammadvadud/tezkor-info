from rest_framework import serializers

from core.apps.main.models import LegalDocumentsModels


class BaseLegalDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalDocumentsModels
        fields = [
            'id',
            'name',
            'file',
            'type',
        ]


class ListLegalDocumentsSerializer(BaseLegalDocumentsSerializer):
    class Meta(BaseLegalDocumentsSerializer.Meta): ...


class RetrieveLegalDocumentsSerializer(BaseLegalDocumentsSerializer):
    class Meta(BaseLegalDocumentsSerializer.Meta): ...


class CreateLegalDocumentsSerializer(BaseLegalDocumentsSerializer):
    class Meta(BaseLegalDocumentsSerializer.Meta):
        fields = [
            "id",
            "name",
        ]
