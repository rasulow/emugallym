from django.db import models
import os


class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    user = models.IntegerField()
    price = models.FloatField()
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Topic(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField()
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
class Lesson(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material = models.FileField(upload_to='lessons/', blank=True, null=True)
    order = models.IntegerField()
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        if self.material:
            if os.path.isfile(self.material.path):
                os.remove(self.material.path)
        super().delete(*args, **kwargs) 
    

    