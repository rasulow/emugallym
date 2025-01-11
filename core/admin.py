from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin
from . import forms


class UserAdmin(ModelAdmin):
    model = User
    list_display = ['username', 'email', 'type', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']

admin.site.register(User, UserAdmin)