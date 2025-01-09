from rest_framework import serializers
from core import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'fullname', 'biography', 'order', 'slug', 'is_active')
        read_only_fields = ('slug',)
        

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Genre
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)
    
    
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Book
        fields = ('title', 'description', 'authors', 'genres', 'price', 
                  'discount', 'price_discount', 'file', 'cover', 'pages', 'reading_time',
                  'published_year', 'age_restriction', 'date_of_writing', 'isbn', 'translator',
                  'book', 'img', 'ext', 'book_size', 'order', 'slug', 'is_active')
        read_only_fields = ('slug', 'created_at', 'updated_at')
    