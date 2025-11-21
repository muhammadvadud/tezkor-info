from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.apps.accounts.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "name",
        ]


class UserSerializer(serializers.ModelSerializer):
    activate_types = CategorySerializer(many=True)

    class Meta:
        exclude = [
            "created_at",
            "updated_at",
            "password",
            "groups",
            "user_permissions",
        ]
        model = get_user_model()


class UserUpdateSerializer(serializers.ModelSerializer):
    activate_types = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CategoryModel.objects.all(),
        write_only=True
    )

    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name",
            "activate_types"
        ]

    def update(self, instance, validated_data):
        activate_types = validated_data.pop("activate_types", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if activate_types is not None:
            instance.activate_types.set(activate_types)
        return instance
