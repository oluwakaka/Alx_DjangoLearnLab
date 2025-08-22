from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Book


# ================================
# Custom User Admin
# ================================
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "date_of_birth", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "date_of_birth", "profile_photo")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2", "date_of_birth", "profile_photo", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)


# ================================
# Book Admin
# ================================
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date")
    search_fields = ("title", "author")


# Register models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Book, BookAdmin)
