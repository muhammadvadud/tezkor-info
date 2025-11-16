from django import forms

from core.apps.main.models import ProductServiceModel


class ProductServiceForm(forms.ModelForm):

    class Meta:
        model = ProductServiceModel
        fields = "__all__"
