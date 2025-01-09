from rest_framework import serializers
from core import models


class AuthorSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'fullname', 'biography', 'order', 'slug', 'is_active')
        read_only_fields = ('slug',)
        

class GenreSerializers(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Genre
        fields = ('id', 'title', 'parent', 'order', 'slug', 'is_active', 'children')
        read_only_fields = ('slug', 'children')
        
    def get_children(self, obj):
        if obj.children.exists():
            return GenreSerializers(obj.children.all(), many=True).data
        return None
    
    
class BookSerializers(serializers.ModelSerializer):
    genre = GenreSerializers()
    
    class Meta:
        model = models.Book
        fields = ('title', 'description', 'authors', 'genres', 'price', 
                  'discount', 'price_discount', 'file', 'cover', 'published_at', 
                  'book', 'img', 'ext', 'book_size', 'order', 'slug', 'is_active')
        read_only_fields = ('id', 'title', 'description', 'authors', 'genres', 'price', 
                            'discount', 'price_discount', 'published_at', 'slug', 'book', 
                            'img', 'ext', 'book_size', 'order', 'is_active')
        write_only_fields = ('title', 'description', 'author', 'genre', 'price', 
                             'discount', 'published_at', 'file', 'cover', 'order', 'is_active')
    