from django.contrib import admin
from django.conf import settings
import requests
from unfold.admin import ModelAdmin
from . import models


@admin.register(models.Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    exclude = ('created_at', 'updated_at', 'slug',)


@admin.register(models.Level)
class LevelAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')


@admin.register(models.Language)
class LanguageAdmin(ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    

@admin.register(models.Course)
class CourseAdmin(ModelAdmin):
    list_display = ('title', 'description', 'get_user', 'price', 'course_duration', 'is_active')
    exclude = ('created_at', 'updated_at', 'slug', 'hours', 'minutes', 'seconds')
    
    def get_user(self, obj):
        try:
            response = requests.get(f'{settings.USERS_SERVICE_URL}/api/users/{obj.user}/')
            if response.status_code == 200:
                user_data = response.json()
                return user_data['email']
            return 'User not found'
        except requests.RequestException as e:
            return str(e)
        
        
            


@admin.register(models.Topic)
class TopicAdmin(ModelAdmin):
    list_display = ('title', 'course', 'order', 'topic_duration', 'is_active')
    exclude = ('created_at', 'updated_at', 'slug', 'hours', 'minutes', 'seconds')
    
    
@admin.register(models.Lesson)
class LessonAdmin(ModelAdmin):
    list_display = ('title', 'topic', 'course', 'type', 'lesson_duration', 'is_active')
    exclude = ('created_at', 'updated_at', 'slug', 'hours', 'minutes', 'seconds')