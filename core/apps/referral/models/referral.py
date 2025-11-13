from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.contrib.auth import get_user_model


class ReferralModel(AbstractBaseModel):
    code = models.CharField(verbose_name=_("code"), max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    referral_registered_count = models.IntegerField(verbose_name=_("referral registered count"), default=0)
    referral_posted_ads_count = models.IntegerField(verbose_name=_("referral posted ads count"), default=0)
    referral_income_amount = models.IntegerField(verbose_name=_("referral income amount"), default=0)

    def __str__(self):
        return str(self.pk)

    @classmethod
    def _baker(cls):
        return baker.make(cls)

    class Meta:
        db_table = "referral"
        verbose_name = _("ReferralModel")
        verbose_name_plural = _("ReferralModels")


class ReferralReward(AbstractBaseModel):
    amount = models.PositiveBigIntegerField(verbose_name=_("amount"), default=0)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "referral_reward"
        verbose_name = _("ReferralReward")
        verbose_name_plural = _("ReferralRewards")
