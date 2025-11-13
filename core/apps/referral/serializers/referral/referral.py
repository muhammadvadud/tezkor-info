from rest_framework import serializers

from core.apps.referral.models import ReferralModel
import random
import string


def generate_code(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


class BaseReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferralModel
        fields = [
            "id",
            "code",
            "user",
            "referral_registered_count",
            "referral_posted_ads_count",
            "referral_income_amount",
        ]


class ListReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta): ...


class RetrieveReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta): ...


class CreateReferralSerializer(BaseReferralSerializer):
    class Meta(BaseReferralSerializer.Meta):
        fields = [
            "id",
            "code",
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context["request"].user
        code = validated_data.get('code')
        if code:
            if code != "generate":
                if len(code) > 6:
                    raise serializers.ValidationError({"code": "Code must be less than 6 characters"})
                check = ReferralModel.objects.filter(code=code).exists()
                if check:
                    raise serializers.ValidationError({"code": "Code already exists"})
                else:
                    return ReferralModel.objects.create(**validated_data)
            else:
                while True:
                    code = generate_code()
                    if not ReferralModel.objects.filter(code=code).exists():
                        validated_data['code'] = code
                        break
                referral_code = ReferralModel.objects.create(**validated_data)
                return referral_code
        else:
            raise serializers.ValidationError({"code": "Code does not exist"})
