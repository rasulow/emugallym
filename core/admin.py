from django import forms
from django.contrib import admin
from django.conf import settings
import requests
from unfold.admin import ModelAdmin
from .models import Course, Category, Level, Language, Topic, Lesson

# Admin for Category
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')

# Admin for Level
@admin.register(Level)
class LevelAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')

# Admin for Language
@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')

# Custom Form for CourseAdmin
class CourseAdminForm(forms.ModelForm):
    user = forms.ChoiceField(choices=[], label="User")  # Add a label to the ChoiceField

    class Meta:
        model = Course
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Fetch users from external user-service
        try:
            response = requests.get(f'{settings.USERS_SERVICE_URL}/api/users/')
            if response.status_code == 200:
                users = response.json()
                # Populate the select field with user email and ID
                user_choices = [(user['id'], user['email']) for user in users]
                self.fields['user'].choices = user_choices
            else:
                self.fields['user'].choices = []  # If no users, set empty choices
        except requests.RequestException:
            self.fields['user'].choices = []  # Handle request failure

# Admin for Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ('title', 'description', 'get_user', 'price', 'is_active', 'created_at', 'updated_at')

    def get_user(self, obj):
        """Fetches and displays the user's email from the external user-service."""
        try:
            response = requests.get(f'{settings.USERS_SERVICE_URL}/api/users/{obj.user}/')
            if response.status_code == 200:
                user_data = response.json()
                return user_data.get('email', 'Unknown user')  # Handle case where email is missing
            return 'User not found'
        except requests.RequestException as e:
            return f'Error: {e}'

# Admin for Topic
@admin.register(Topic)
class TopicAdmin(ModelAdmin):
    list_display = ('title', 'course', 'order', 'is_active')

# Admin for Lesson
@admin.register(Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ('title', 'topic', 'course', 'type', 'order', 'is_active')
