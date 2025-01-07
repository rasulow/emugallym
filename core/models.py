import uuid
from django.db import models
from django.utils.text import slugify
import os


class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
        
    class Meta:
        db_table = 'category'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['-created_at']
        
        
class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        db_table = 'level'
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'
        ordering = ['-created_at']
        
        
class Language(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    class Meta:
        db_table = 'languages'
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'
        ordering = ['-created_at']
    

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.IntegerField()
    category = models.ManyToManyField(Category, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='course/thumbnail/', blank=True, null=True)
    preview_video = models.FileField(upload_to='course/preview/', blank=True, null=True)
    paid = models.BooleanField(default=False)
    price = models.FloatField()
    discount = models.FloatField(default=0)
    certified = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
        
    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
    
    
class Topic(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    order = models.IntegerField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
    
    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-created_at']
    
    
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material = models.FileField(upload_to='lessons/', blank=True, null=True)
    order = models.IntegerField()
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        if self.material:
            if os.path.isfile(self.material.path):
                os.remove(self.material.path)
        super().delete(*args, **kwargs) 
        
        
    class Meta:
        db_table = 'lesson'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['-created_at']
        
    
    

    