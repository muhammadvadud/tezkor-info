from django import forms

from core.apps.payments.models import CashbackModel


class CashbackForm(forms.ModelForm):

    class Meta:
        model = CashbackModel
        fields = "__all__"
