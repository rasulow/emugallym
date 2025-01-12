from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify
import uuid

class UserManager(BaseUserManager):
    
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        
        if password:
            user.set_password(password)  # Ensure password is hashed
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)
        
        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must be assigned to is_staff=True.')
        
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must be assigned to is_superuser=True.')
        
        return self.create_user(email, password, **kwargs)

    
    
class Profession(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'profession'
        verbose_name = 'Profession'
        verbose_name_plural = 'Professions'
        ordering = ['order']
    
    
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('instructor', 'Instructor'),
        ('student', 'Student'),
    )
    
    username = models.CharField(max_length=30, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=10, null=True, blank=True)
    type = models.CharField(max_length=10, choices=USER_TYPE, null=True, blank=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    middle_name = models.CharField(max_length=30, null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    profession = models.ForeignKey(Profession, on_delete=models.SET_NULL, null=True, blank=True)
    phone_number = models.CharField(max_length=30, null=True, blank=True)
    img = models.ImageField(upload_to='profile/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='profile-thumbnail/', blank=True, null=True)
    slug = models.SlugField(max_length=250, unique=True, blank=True, null=True)
    order = models.IntegerField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_sha256'):
            self.password = make_password(self.password)
            
        if not self.slug:
            self.slug = slugify(str(uuid.uuid4()))
            
        super().save(*args, **kwargs)
        
    def fullname(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"
        