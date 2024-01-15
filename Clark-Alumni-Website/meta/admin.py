from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import gettext_lazy as _

from meta.models import StudentRequestForm, User


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "academic_standing", "cell_phone")},
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
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "cell_phone",
                    "academic_standing",
                    "groups",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = (
        "first_name",
        "last_name",
        "email",
        "academic_standing",
        "cell_phone",
    )
    ordering = ("email",)


admin.site.register(StudentRequestForm)
