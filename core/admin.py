from django.contrib import admin
from .models import User, Profession
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


class ProfessionAdmin(ModelAdmin):
    model = Profession
    list_display = ['title', 'slug', 'order', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['title']
    ordering = ['order']

admin.site.register(Profession, ProfessionAdmin)
    