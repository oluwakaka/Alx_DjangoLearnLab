from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Use email instead of username
    ordering = ("email",)
    list_display = ("email", "date_of_birth", "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("email", "password", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "date_of_birth", "profile_photo", "password1", "password2"),
        }),
    )
    search_fields = ("email",)

admin.site.register(User, UserAdmin)
