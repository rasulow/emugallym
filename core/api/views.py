from rest_framework import viewsets, filters
from rest_framework.parsers import MultiPartParser, FormParser
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from core import models
from . import serializers
from .filters import CourseFilter


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    lookup_field = 'slug'
    

class CourseViewSet(viewsets.ModelViewSet):
    queryset = models.Course.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CourseFilter
    search_fields = ['title']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CourseDetailSerializer 
        elif self.action == 'list':
            return serializers.CourseListSerializer
        elif self.action == 'create':
            return serializers.CourseCreateSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return serializers.CourseCreateSerializer
        return serializers.CourseDetailSerializer  


class TopicViewSet(viewsets.ModelViewSet):
    queryset = models.Topic.objects.all()
    serializer_class = serializers.TopicSerializer
    lookup_field ='slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course__slug']
    search_fields = ['title']
    ordering_fields = ['order', 'created_at']
    
    
class LessonViewSet(viewsets.ModelViewSet):
    queryset = models.Lesson.objects.all()
    serializer_class = serializers.LessonSerializer
    parser_classes = (MultiPartParser, FormParser)
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['course__slug', 'topic__slug']
    search_fields = ['title']
    ordering_fields = ['order', 'created_at']
    
    
class LevelViewSet(viewsets.ModelViewSet):
    queryset = models.Level.objects.all()
    serializer_class = serializers.LevelSerializer
    lookup_field = 'id'
    
    
class LanguageViewSet(viewsets.ModelViewSet):
    queryset = models.Language.objects.all()
    serializer_class = serializers.LanguageSerializer
    lookup_field = 'id'
    
