from django import forms

from core.apps.main.models import PriceCountryModel


class PriceCountryForm(forms.ModelForm):

    class Meta:
        model = PriceCountryModel
        fields = "__all__"
