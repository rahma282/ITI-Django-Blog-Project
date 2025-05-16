from rest_framework import serializers
from .models import Post, Author, Comments

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'email', 'phone']

    def validate_email(self, value):
        if '@' not in value:
            raise serializers.ValidationError("Invalid email address.")
        return value

class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    class Meta:
        model = Post
        fields = ['id','title', 'content', 'image_url', 'author_id', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

    def validate_title(self, value):
        if not all(c.isalnum() or c.isspace() for c in value):
            raise serializers.ValidationError("Title should only contain letters, numbers and spaces.")
        return value