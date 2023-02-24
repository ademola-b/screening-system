from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class CustomUserAdmin(UserAdmin):
    """Define admin model for custom user model with no username"""
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name","last_name")}),
        (("User Type"), {"fields": ("user_type",)}),
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
                "fields": ("email", "password1", "password2", "user_type"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff", "user_type")
    search_fields = ("email", "first_name", "last_name", "is_staff", "user_type")
    ordering = ('email',)


admin.site.register(get_user_model(), CustomUserAdmin)

# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     add_fieldsets = (
#             (None, {
#                 'classes': ('wide',),
#                 'fields': ('email', 'password1', 'password2', 'user_type'),
#             }),
#         )