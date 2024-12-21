from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from . import forms


class UserAdmin(ModelAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password', 'otp')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

admin.site.register(User, UserAdmin)