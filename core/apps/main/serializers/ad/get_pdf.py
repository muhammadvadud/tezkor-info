from rest_framework import serializers
from core.apps.main.models.ad import AdModel
from core.services.pdf_generate import generate_pdf


class GetPDFSerializer(serializers.ModelSerializer):
    path = serializers.SerializerMethodField()

    class Meta:
        model = AdModel
        fields = [
            'path',
        ]

    def get_path(self, obj):
        if obj.pdf_path is None:
            data = []
            for user in obj.sent_to.all():
                full_name = f"{user.first_name} {user.last_name}"
                company = user.company_name if user.company_name else ""

                data.append({
                    "fish": full_name,
                    "company": company
                })

            path = generate_pdf(data, obj.id)
            obj.pdf_path = path
            obj.save()
            return path
        else:
            return obj.pdf_path
