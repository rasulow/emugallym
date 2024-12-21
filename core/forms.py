from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserAdminForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'is_staff', 'is_active', 'is_superuser') 
