import requests
from rest_framework import serializers
from django.conf import settings
from core import models


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = ('id', 'title', 'order', 'is_active',)
        read_only_fields = ('slug',)
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)
        

class CourseSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(many=True)
    
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'user', 'level',
                  'category', 'thumbnail', 'price', 'discount', 'slug', 
                  'is_active', 'paid', 'certified', 'start_date',)
        read_only_fields = ('slug',)
        
        
        
    def validate_user(self, value):
        response = requests.get(f'{settings.USERS_SERVICE_URL}/api/users/{value}/')
        if response.status_code != 200:
            raise serializers.ValidationError('User not found')
        return value
    
    
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'course', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)
        


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'title', 'topic', 'course', 'order', 'material', 'slug', 'is_active',)
        read_only_fields = ('slug',)
        
        