import uuid

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class User(models.Model):
    class AccountTiers(models.TextChoices):
        BASIC = _("Basic")
        PREMIUM = _("Premium")
        ENTERPRISE = _("Enterprise")

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, primary_key=True, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    tier = models.CharField(
        blank=False,
        choices=AccountTiers.choices,
        max_length=10,
        default=AccountTiers.BASIC,
    )
