from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, identifier, password=None, **extra_fields):
        if not identifier:
            raise ValueError("The identifier field must be set.")

        if "@" in identifier:
            extra_fields.setdefault("email", identifier)
        else:
            extra_fields.setdefault("phone_number", identifier)

        user = self.model(identifier=identifier, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(identifier, password, **extra_fields)


class CustomUser(AbstractUser, PermissionsMixin):
    identifier = models.CharField(
        max_length=255, unique=True, verbose_name=_("identifier")
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
        verbose_name=_("phone_number"),
    )
    email = models.EmailField(
        blank=True, null=True, unique=True, verbose_name=_("email")
    )
    is_active = models.BooleanField(default=True, verbose_name=_("is_active"))
    is_staff = models.BooleanField(default=False, verbose_name=_("is_staff"))
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("date_joined"))

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.identifier
