from django_core.models import AbstractBaseModel
from model_bakery import baker
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class PriceBracketModel(AbstractBaseModel):
    name = models.CharField(max_length=255, blank=True, help_text="(ixtiyoriy) Bracket nomi, masalan '1-10'")
    min_people = models.PositiveIntegerField()
    max_people = models.PositiveIntegerField()
    price_per_person = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0, help_text="Ko'rsatish tartibi. Kichikroq oldin.")

    class Meta:
        ordering = ["order", "min_people"]
        verbose_name = "Price bracket"
        verbose_name_plural = "Price brackets"
        constraints = [
            models.CheckConstraint(check=models.Q(max_people__gte=models.F('min_people')), name='max_gte_min')
        ]

    def clean(self):
        if self.min_people > self.max_people:
            raise ValidationError(_("min_people must be <= max_people"))

        overlaps = PriceBracketModel.objects.filter(
            active=True
        ).exclude(pk=self.pk).filter(
            min_people__lte=self.max_people,
            max_people__gte=self.min_people
        )
        if overlaps.exists():
            raise ValidationError(
                _("This bracket overlaps with existing active brackets: %s") % ", ".join([str(o.pk) for o in overlaps]))

    def __str__(self):
        return self.name or f"{self.min_people}-{self.max_people}: {self.price_per_person}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
