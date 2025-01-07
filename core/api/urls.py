from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'category', views.CategoryViewSet)
router.register(r'courses', views.CourseViewSet)
router.register(r'topics', views.TopicViewSet)
router.register(r'lesson', views.LessonViewSet)
router.register(r'level', views.LevelViewSet)


urlpatterns = [
    path('', include(router.urls)),
]