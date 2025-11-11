from django.contrib.auth import models as auth_models
from django.db import models
from .region import District
from ..choices import RoleChoice, PersonTypeChoice
from ..managers import UserManager
from core.apps.main.models import ActivateTypesModel


class User(auth_models.AbstractUser):
    phone = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    validated_at = models.DateTimeField(null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, blank=True, null=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    stir = models.CharField(max_length=255, null=True, blank=True)
    director_full_name = models.CharField(max_length=255, null=True, blank=True)
    role = models.CharField(
        max_length=255,
        choices=RoleChoice,
        default=RoleChoice.USER,
    )
    person_type = models.CharField(
        max_length=255,
        choices=PersonTypeChoice,
        default=PersonTypeChoice.INDIVIDUAL,

    )
    activate_types = models.ManyToManyField(ActivateTypesModel, blank=True)
    USERNAME_FIELD = "phone"
    objects = UserManager()

    def __str__(self):
        return self.phone
