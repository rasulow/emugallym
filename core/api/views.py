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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.CourseDetailSerializer
        elif self.action == 'list':
            return serializers.CourseListSerializer
        elif self.action == 'create':
            return serializers.CourseCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return serializers.CourseCreateSerializer
        return serializers.CourseDetailSerializer

    @swagger_auto_schema(
        operation_description="List courses with optional filtering",
        manual_parameters=[
            # Define filter parameters explicitly
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Comma-separated list of categories to filter by",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'paid',
                openapi.IN_QUERY,
                description="Filter by paid status (true/false)",
                type=openapi.TYPE_BOOLEAN,
            ),
            openapi.Parameter(
                'user',
                openapi.IN_QUERY,
                description="Filter by user ID",
                type=openapi.TYPE_INTEGER,
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search by title",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order the results (e.g., title)",
                type=openapi.TYPE_STRING,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = models.Course.objects.all()

        # Filtering by category (using 'category__slug')
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug__in=category.split(','))

        # Filtering by paid status
        paid = self.request.query_params.get('paid')
        if paid is not None:
            queryset = queryset.filter(paid=paid.lower() == 'true')

        # Filtering by user ID
        user = self.request.query_params.get('user')
        if user:
            queryset = queryset.filter(user=user)

        return queryset


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
    
