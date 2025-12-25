from django.db import models
from django_core.models.base import AbstractBaseModel
from django.utils.translation import gettext_lazy as _
from core.apps.main.choices.legal_documents import LegalDocumentsChoices


class LegalDocumentsModels(AbstractBaseModel):
    name = models.CharField(verbose_name=_('Name'), max_length=100)
    file = models.FileField(upload_to='legal_documents/')
    type = models.CharField(verbose_name=_('Type'), max_length=100, choices=LegalDocumentsChoices)

    def __str__(self):
        return str(self.pk)

    class Meta:
        db_table = 'legal_documents'
        verbose_name = _('Legal Documents')
        verbose_name_plural = _('Legal Documents')
