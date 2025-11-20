from rest_framework import serializers

from core.apps.main.models import PriceCountryModel


class PriceCalculateSerializer(serializers.Serializer):
    country = serializers.CharField()
    region = serializers.CharField()
    district = serializers.CharField()
    letters = serializers.CharField()

#
# class PriceCalculationSerializer(serializers.Serializer):
#     people_count = serializers.IntegerField(write_only=True)
#     price_per_person = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
#     total_price = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)
#     range = serializers.CharField(read_only=True)
#
#     def validate_people_count(self, value):
#         if value is None:
#             raise serializers.ValidationError("people_count required")
#         if value <= 0:
#             raise serializers.ValidationError("people_count must be > 0")
#         return value
#
#     def create(self, validated_data):
#         people_count = validated_data['people_count']
#
#         bracket = (
#             PriceBracketModel.objects.filter(
#                 active=True,
#                 min_people__lte=people_count,
#                 max_people__gte=people_count
#             )
#             .order_by("order", "min_people")
#             .first()
#         )
#
#         if not bracket:
#             raise serializers.ValidationError({"detail": f"{people_count} ta odam uchun narx topilmadi"})
#
#         price_per_person = Decimal(bracket.price_per_person)
#         total_price = price_per_person * Decimal(people_count)
#         result = {
#             "people_count": people_count,
#             "price_per_person": price_per_person,
#             "total_price": total_price,
#             "range": f"{bracket.min_people} - {bracket.max_people}",
#         }
#         return result
#
#     def to_representation(self, instance):
#
#         data = instance or getattr(self, "validated_data", None)
#         if not data:
#             return {}
#         return {
#             "people_count": data["people_count"],
#             "price_per_person": str(data["price_per_person"]),
#             "total_price": str(data["total_price"]),
#             "range": data["range"],
#         }
