from django.contrib import admin
from . import models
from unfold.admin import ModelAdmin


@admin.register(models.Author)
class AuthorAdmin(ModelAdmin):
    list_display = ('fullname', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('fullname', 'biography')
    
    
@admin.register(models.Genre)
class GenreAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title',)


@admin.register(models.Tag)
class TagAdmin(ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('title',)
    
    
    
@admin.register(models.Book)
class BookAdmin(ModelAdmin):
    list_display = ('title', 'pages', 'book_size', 'ext', 'is_active')
    list_filter = ('genre', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'author__fullname', 'genre__title')
    