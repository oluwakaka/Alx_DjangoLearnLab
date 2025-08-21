from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import *  # Import your relationship_app models if any

User = get_user_model()  # This will now point to accounts.CustomUser

class CustomUserAdmin(DjangoUserAdmin):
    # This reuses the default UserAdmin, but works with our custom user model
    fieldsets = DjangoUserAdmin.fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (None, {'fields': ('date_of_birth', 'profile_photo')}),
    )

# Register CustomUser here without duplication
if not admin.site.is_registered(User):
admin.site.register(User, CustomUserAdmin)
