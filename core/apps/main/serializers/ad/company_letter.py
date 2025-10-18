from rest_framework import serializers
from django.contrib.auth import get_user_model


class CompanyLetterSummarySerializer(serializers.Serializer):
    letters = serializers.CharField(write_only=True)
    used_letters = serializers.ListField(child=serializers.CharField(), read_only=True)
    total_count = serializers.IntegerField(read_only=True)

    def validate_letters(self, value):
        letters = [l.strip().upper() for l in value.split(',') if l.strip()]
        if not letters:
            raise serializers.ValidationError("Hech bo'lmaganda bitta harf kiriting.")
        return letters

    def create(self, validated_data):
        return validated_data

    def to_representation(self, instance):
        letters = instance.get("letters", [])

        used = []
        total_count = 0

        for l in letters:
            count = get_user_model().objects.filter(company_name__istartswith=l).count()
            if count > 0:
                used.append(l)
                total_count += count

        return {
            "used_letters": used,
            "total_count": total_count,
        }
