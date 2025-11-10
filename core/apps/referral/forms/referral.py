from django import forms

from core.apps.referral.models import ReferralModel


class ReferralForm(forms.ModelForm):

    class Meta:
        model = ReferralModel
        fields = "__all__"
