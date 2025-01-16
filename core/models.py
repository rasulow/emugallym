import uuid
from django.db import models
from django.utils.text import slugify
import os
from ckeditor.fields import RichTextField
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from .utils import normalize_time





class Category(models.Model):
    title = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
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
    order = models.IntegerField(blank=True, null=True)
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
    order = models.IntegerField(blank=True, null=True)
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
    short_description = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    learning_outcomes = RichTextField(blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    user = models.IntegerField()
    category = models.ManyToManyField(Category, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='course/thumbnail/', blank=True, null=True)
    preview_video = models.FileField(upload_to='course/preview/', blank=True, null=True)
    paid = models.BooleanField(default=False)
    price = models.FloatField(default=0)
    discount = models.FloatField(default=0)
    certified = models.BooleanField(default=False)
    start_date = models.DateTimeField(blank=True, null=True)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    seconds = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
    def course_duration(self):
        if self.hours == 0:
            return f'{self.minutes:02d}:{self.seconds:02d}'
        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
        
        
    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
    
    
class Topic(models.Model):
    title = models.CharField(max_length=255)
    course = models.ForeignKey(Course, related_name='topics', on_delete=models.CASCADE)
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    seconds = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
        super().save(*args, **kwargs)
        
    def topic_duration(self):
        if self.hours == 0:
            return f'{self.minutes:02d}:{self.seconds:02d}'
        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
        
    
    class Meta:
        db_table = 'topic'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        ordering = ['-created_at']
    
    
class Lesson(models.Model):
    TYPES = (
        ('video', 'Video'),
        ('document', 'Document'),
    )
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    material = models.FileField(upload_to='lessons/', blank=True, null=True)
    type = models.CharField(max_length=10, choices=TYPES, default='video')
    hours = models.IntegerField(default=0)
    minutes = models.IntegerField(default=0)
    seconds = models.IntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))

        if self.type == 'video':
            try:
                video_path = self.material.path
                clip = VideoFileClip(video_path)
                duration_in_seconds = clip.duration
                
                hours = int(duration_in_seconds // 3600)
                minutes = int((duration_in_seconds % 3600) // 60)
                seconds = int(duration_in_seconds % 60)
                
                self.hours, self.minutes, self.seconds = normalize_time(hours, minutes, seconds)
                
                self.topic.hours, self.topic.minutes, self.topic.seconds = normalize_time(
                    self.topic.hours + self.hours,
                    self.topic.minutes + self.minutes,
                    self.topic.seconds + self.seconds
                )
                self.topic.save()

                self.course.hours, self.course.minutes, self.course.seconds = normalize_time(
                    self.course.hours + self.hours,
                    self.course.minutes + self.minutes,
                    self.course.seconds + self.seconds
                )
                self.course.save()

            except Exception as e:
                print(f"Error processing video: {e}")
                
        super().save(*args, **kwargs)
        
        
    def delete(self, *args, **kwargs):
        if self.material:
            if os.path.isfile(self.material.path):
                os.remove(self.material.path)
        super().delete(*args, **kwargs) 
        
    def lesson_duration(self):
        if self.hours == 0:
            return f'{self.minutes:02d}:{self.seconds:02d}'
        return f'{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}'
        
        
    class Meta:
        db_table = 'lesson'
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'
        ordering = ['-created_at']
        
    
    

    