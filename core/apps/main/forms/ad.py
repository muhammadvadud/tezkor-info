from core.apps.main.models import AdModel
from django import forms


class AdForm(forms.ModelForm):
    class Meta:
        model = AdModel
        fields = "__all__"
