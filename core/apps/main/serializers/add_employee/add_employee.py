from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class BaseEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'phone',
        ]


class ListEmployeeSerializer(BaseEmployeeSerializer):
    class Meta(BaseEmployeeSerializer.Meta): ...


class RetrieveEmployeeSerializer(BaseEmployeeSerializer):
    class Meta(BaseEmployeeSerializer.Meta): ...


class CreateEmployeeSerializer(BaseEmployeeSerializer):
    class Meta(BaseEmployeeSerializer.Meta):
        fields = [
            'first_name',
            'last_name',
            'phone',
        ]

    def validate(self, data):
        phone = data.get('phone')
        check = get_user_model().objects.filter(phone=phone).exists()
        if check:
            raise serializers.ValidationError(_("Uzr bunday raqamdagi foydalanuvchi allaqachon mavjud"))
        return data

    def create(self, validated_data):
        validated_data['parent'] = self.context['request'].user
        user = get_user_model().objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        return user
