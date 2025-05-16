from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, status, serializers
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view

from .models import Post, Author
from .serializers import PostSerializer

# ------------------- API Views -------------------

class PostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  

    def get_queryset(self):
        print("User:", self.request.user)
        print("Auth:", self.request.auth) 
        return Post.objects.all()

    def perform_create(self, serializer):
        print("Authenticated user:", self.request.user)
        try:
            author = Author.objects.get(user=self.request.user)
        except Author.DoesNotExist:
            raise serializers.ValidationError("No matching Author for the authenticated user.")
        serializer.save(author=author)

class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

# ------------------- Auth Serializers and Views -------------------

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    name = serializers.CharField(required=False, allow_blank=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already registered")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('name', '')
        )
        Author.objects.create(
            user=user,
            name=user.first_name or "Anonymous",
            email=user.email
        )
        return user

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.first_name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APILoginView(APIView):
    def post(self, request):
        data = request.data
        print("Login request data:", request.data)
        user = authenticate(username=data.get('email'), password=data.get('password'))
        if user is None:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        refresh = RefreshToken.for_user(user)
        return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)

@api_view(['GET'])
def check_email(request):
    email = request.query_params.get('email', None)
    if email is None:
        return Response({'error': 'Email query param is required'}, status=status.HTTP_400_BAD_REQUEST)
    exists = User.objects.filter(email=email).exists()
    return Response({'exists': exists})
