from core.apps.main.models import ActivateTypesModel
from django import forms


class ActivateTypesForm(forms.ModelForm):

    class Meta:
        model = ActivateTypesModel
        fields = "__all__"
