from django.db import models
from django.utils.text import slugify
import os
import uuid


class Author(models.Model):
    fullname = models.CharField(max_length=255)
    biography = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'author'
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
        ordering = ['order']
        
    def __str__(self):
        return self.fullname
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.fullname)
        super().save(*args, **kwargs)
        
    
class Genre(models.Model):
    title = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'genre'
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['order']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
        
class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    author = models.ManyToManyField(Author)
    genre = models.ManyToManyField(Genre)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.IntegerField(default=0)
    file = models.FileField(upload_to='books/')
    cover = models.ImageField(upload_to='covers/')
    pages = models.IntegerField(blank=True, null=True)  # Number of printed pages
    reading_time = models.CharField(max_length=50, blank=True, null=True)  # Estimated reading time
    published_year = models.IntegerField(blank=True, null=True)  # Year of publication
    age_restriction = models.CharField(max_length=10, blank=True, null=True)  # Age restriction (e.g., "16+")
    date_of_writing = models.DateField(blank=True, null=True)  # Date the book was written
    isbn = models.CharField(max_length=20, blank=True, null=True)  # ISBN (EAN) number
    translator = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'book'
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['order']
        
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Handle file and cover renaming before saving
        if self.cover:
            filename = '{}.{}'.format(str(uuid.uuid4()), self.cover.name.split('.')[-1])
            self.cover.name = os.path.join('covers', filename)

        if self.file:
            filename = '{}.{}'.format(str(uuid.uuid4()), self.file.name.split('.')[-1])
            self.file.name = os.path.join('books', filename)

        # Now save the instance
        super().save(*args, **kwargs)
        
    def book(self):
        if self.file:
            return self.file.url
        return None
    
    def img(self):
        if self.cover:
            return self.cover.url
        return None
    
    def price_discount(self):
        return self.price - (self.price * self.discount / 100)
    
    def authors(self):
        return [str(author) for author in self.author.all()]
    
    def genres(self):
        return [str(genre) for genre in self.genre.all()]
    
    def book_size(self):
        size_in_mb = self.file.size / (1024 * 1024)
        return "{:.2f} MB".format(size_in_mb)
    
    def ext(self):
        ext = self.file.name.split('.')[-1]
        return f".{ext}"
    