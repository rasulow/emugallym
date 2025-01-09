from rest_framework import serializers
from core import models


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('id', 'fullname', 'biography', 'order', 'slug', 'is_active')
        read_only_fields = ('slug',)
        

class GenreSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Genre
        fields = ('id', 'title', 'parent', 'order', 'slug', 'is_active', 'children')
        read_only_fields = ('slug', 'children')
        
    def get_children(self, obj):
        children = obj.genre_set.all()
        if children.exists():
            return GenreSerializer(children, many=True).data 
        return None
    
    
class BookSerializer(serializers.ModelSerializer):
    # genres = GenreSerializer()
    
    class Meta:
        model = models.Book
        fields = ('title', 'description', 'authors', 'genres', 'price', 
                  'discount', 'price_discount', 'file', 'cover', 'published_at', 
                  'book', 'img', 'ext', 'book_size', 'order', 'slug', 'is_active')
        read_only_fields = ('slug', 'created_at', 'updated_at')
    