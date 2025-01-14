import requests
from rest_framework import serializers
from django.conf import settings
from core import models


class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Level
        fields = ('id', 'title', 'order', 'is_active',)
        
        
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ('id', 'title', 'order', 'is_active',)
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)
     
        
class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ('id', 'title', 'topic', 'course', 'order', 'material', 'type', 'lesson_duration', 'slug', 'is_active',)
        read_only_fields = ('slug', 'lesson_duration',)    
        
        
class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True)
    
    class Meta:
        model = models.Topic
        fields = ('id', 'title', 'course', 'order', 'topic_duration', 'lessons', 'slug', 'is_active',)
        read_only_fields = ('slug', 'lessons', 'topic_duration',)
        
        
class CourseCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'user', 'level', 'language',
                  'category', 'thumbnail', 'price', 'discount', 'slug', 
                  'is_active', 'paid', 'certified', 'start_date',)
        read_only_fields = ('slug',)
        
        
        
    def validate_user(self, value):
        response = requests.get(f'{settings.USERS_SERVICE_URL}/api/user/{value}/')
        if response.status_code != 200:
            raise serializers.ValidationError('User not found')
        return value
    
    
class CourseListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)
    
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'short_description', 'description', 'learning_outcomes', 'user', 
                  'requirements', 'level', 'language', 'category', 'thumbnail', 'price', 'discount',
                  'course_duration', 'slug', 'is_active', 'paid', 'certified', 'start_date',)
        read_only_fields = ('slug', 'course_duration')
        
        
        
    def validate_user(self, value):
        response = requests.get(f'{settings.USERS_SERVICE_URL}/api/user/{value}/')
        if response.status_code != 200:
            raise serializers.ValidationError('User not found')
        return value
    
    
    def get_user(self, obj):
        user_id = obj.user 
        try:
            response = requests.get(f"{settings.USERS_SERVICE_URL}/api/user/{user_id}")
            if response.status_code == 200:
                return response.json() 
            return None
        except requests.RequestException:
            return None
        
        
    
class CourseDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True)
    topics = TopicSerializer(many=True)
    level = LevelSerializer()
    language = LanguageSerializer()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'short_description', 'description', 'learning_outcomes', 'user', 'requirements', 
                  'level', 'language', 'category', 'thumbnail', 'preview_video', 'price', 'discount', 
                  'course_duration', 'slug', 'is_active', 'paid', 'certified', 'start_date', 'topics',)
        read_only_fields = ('slug', 'course_duration')
        
    def get_user(self, obj):
        user_id = obj.user 
        try:
            response = requests.get(f"{settings.USERS_SERVICE_URL}/api/user/{user_id}")
            if response.status_code == 200:
                return response.json() 
            return None
        except requests.RequestException:
            return None