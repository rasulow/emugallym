import requests
from rest_framework import serializers
from django.conf import settings
from core import models


class CourseSerizlizer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'user', 'price', 'is_active',)
        
        # def validate_user(self, value):
            