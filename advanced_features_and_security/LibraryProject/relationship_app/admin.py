from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'location')  # adjust fields to your model
    search_fields = ('user__username', 'bio', 'location')
