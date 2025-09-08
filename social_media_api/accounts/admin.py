from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User  # import your custom user model


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ("username", "email", "is_staff", "is_active")
    search_fields = ("username", "email")

    # Only include ManyToManyFields here
    filter_horizontal = ("groups", "user_permissions")  # remove anything else
