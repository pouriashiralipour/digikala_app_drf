from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    username = None
    phone_number = models.CharField(_("phone_number"), max_length=11)
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["phone_number"]
