from django.db import models
from django.utils.translation import gettext_lazy as _


class SignupBonusModel(models.Model):
    amount = models.PositiveBigIntegerField(default=0, verbose_name=_('Amount'))

    def __str__(self):
        return str(self.amount)

    class Meta:
        db_table = 'account_signup_bonus'
        verbose_name = _('Signup Bonus')
        verbose_name_plural = _('Signup Bonus')
