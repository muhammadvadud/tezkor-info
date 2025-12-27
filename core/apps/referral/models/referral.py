from django.db import models
from django.utils.translation import gettext_lazy as _
from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class ReferralModel(AbstractBaseModel):
    code = models.CharField(verbose_name=_("code"), max_length=255, unique=True)
    user = models.ForeignKey(get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    referral_registered_count = models.IntegerField(verbose_name=_("referral registered count"), default=0)
    referral_income_amount = models.IntegerField(verbose_name=_("referral income amount"), default=0)
    referral_share = models.IntegerField(verbose_name=_("referral share %"), default=0)
    description = models.TextField(verbose_name=_("description"), blank=True, null=True)
    is_agent = models.BooleanField(verbose_name=_("is_agent"), default=False)
    referral_earnings = models.PositiveIntegerField(verbose_name=_("referral earnings"), default=0)

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
    min_person = models.IntegerField(verbose_name=_("min_person"), default=0)
    max_person = models.IntegerField(verbose_name=_("max_person"))
    share = models.IntegerField(verbose_name=_("share"), default=0)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = "referral_reward"
        verbose_name = _("ReferralReward")
        verbose_name_plural = _("ReferralRewards")

    def clean(self):
        if self.min_person > self.max_person:
            raise ValidationError(_("min_people must be <= max_people"))

        overlaps = ReferralReward.objects.filter(
            active=True
        ).exclude(pk=self.pk).filter(
            min_people__lte=self.max_person,
            max_people__gte=self.min_person
        )
        if overlaps.exists():
            raise ValidationError(
                _("This bracket overlaps with existing active brackets: %s") % ", ".join([str(o.pk) for o in overlaps]))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
