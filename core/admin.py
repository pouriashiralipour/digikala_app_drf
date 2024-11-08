from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("identifier", "phone_number", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("identifier", "phone_number", "email")
    ordering = ("identifier",)
    readonly_fields = ("date_joined",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "identifier",
                    "phone_number",
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                ),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("identifier", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
