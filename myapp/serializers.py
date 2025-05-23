from rest_framework import serializers
from .models import Post
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PostSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # shows username only

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image_url', 'user', 'created_at']
        read_only_fields = ['user', 'created_at']

    # def validate_title(self, value):
    #     if not value.replace(" ", "").isalnum():  
    #         raise serializers.ValidationError("Title should only contain letters, numbers, and spaces.")
    #     return value


