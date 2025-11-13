from django import forms

from core.apps.referral.models import ReferralHistoryModel


class ReferralHistoryForm(forms.ModelForm):

    class Meta:
        model = ReferralHistoryModel
        fields = "__all__"
