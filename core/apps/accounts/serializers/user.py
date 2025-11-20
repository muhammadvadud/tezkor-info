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
    class Meta:
        model = get_user_model()
        fields = [
            "first_name",
            "last_name"
        ]
