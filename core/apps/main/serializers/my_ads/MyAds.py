from rest_framework import serializers

from core.apps.main.models import AdModel, AdFilesModel, CategoryModel


class AdTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "name",
        ]


class AdFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdFilesModel
        fields = [
            "id",
            "file"
        ]


class BaseMyadsSerializer(serializers.ModelSerializer):
    files = AdFilesSerializer(many=True, read_only=True)
    types = AdTypesSerializer(many=True, read_only=True)
    letters = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = AdModel
        fields = [
            "id",
            "title",
            "description",
            "total_view_count",
            "files",
            "status",
            "types",
            "letters",
            "total_price",
            "phone_number",
            "payments_type",
            "created_at",
            "username",
        ]

    def get_letters(self, obj):
        cls = obj.company_selections.all()
        letters = []

        for l in cls:
            if l.letters not in letters:
                letters.append(l.letters)

        return letters

    def get_username(self, obj):
        return f"{obj.created_by.first_name} {obj.created_by.last_name}"


class ListMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta): ...


class RetrieveMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta): ...


class CreateMyadsSerializer(BaseMyadsSerializer):
    class Meta(BaseMyadsSerializer.Meta):
        fields = [
            "id",
        ]
