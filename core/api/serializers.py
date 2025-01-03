import requests
from rest_framework import serializers
from django.conf import settings
from core import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'user', 'price', 'slug', 'is_active',)
        
    def validate_user(self, value):
        response = requests.get(f'{settings.USERS_SERVICE_URL}/api/users/{value}/')
        if response.status_code != 200:
            raise serializers.ValidationError('User not found')
        return value
    
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'course', 'order', 'slug', 'is_active',)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'title', 'topic', 'course', 'order', 'material', 'slug', 'is_active',)
