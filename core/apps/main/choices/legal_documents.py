from django.db import models
from django.utils.translation import gettext_lazy as _


class LegalDocumentsChoices(models.TextChoices):
    """
    Legal documents choices
    """
    COOKIE_POLICY = ("cookie_policy", _("Cookie siyosati"))
    PRIVACY_POLICY = ("privacy_policy", _("Maxfiylik siyosati"))
    TERMS_OF_USE = ("terms_of_use", _("Foydalanish qoidalari"))
    TERMS_OF_SERVICE = ("terms_of_service", _("Xizmat ko‘rsatish shartlari"))
