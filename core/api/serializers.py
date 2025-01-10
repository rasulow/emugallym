from rest_framework import serializers
from core import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'fullname', 'biography', 'img', 'order', 'slug', 'is_active')
        read_only_fields = ('slug',)
        

class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Genre
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Tag
        fields = ('id', 'title', 'order', 'slug', 'is_active',)
        read_only_fields = ('slug',)
    
    
class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Book
        fields = ('title', 'description', 'authors', 'genres', 'tags', 'file', 'cover', 'paid', 
                  'pages', 'reading_time', 'edition_year', 'published_at', 'age_restriction', 
                  'date_of_writing', 'isbn', 'translator', 'ext', 'book_size', 
                  'order', 'slug', 'is_active')
        read_only_fields = ('slug', 'created_at', 'updated_at')
    