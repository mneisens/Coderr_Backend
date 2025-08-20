from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'type', 'location', 'created_at']
    list_filter = ['user__type', 'created_at']
    search_fields = ['user__username', 'first_name', 'last_name', 'location']
    readonly_fields = ['created_at', 'updated_at']
