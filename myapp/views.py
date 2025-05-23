from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.contrib.auth.models import User
from .models import Post
from .serializers import PostSerializer, RegisterSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework.exceptions import PermissionDenied



# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

# ------------------- API Views -------------------

# List all posts or create a new post
class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Debug print to show who is creating the post
        print("User creating post:", self.request.user)

        # Check if user is authenticated before saving
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Authentication required to create posts.")
    def perform_create(self, serializer):
        print("User creating post:", self.request.user)
        print("Post data:", serializer.validated_data)
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Authentication required to create posts.")


#Retrieve, update, or delete a specific post
class PostDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def put(self, request, *args, **kwargs):  #for debugging
        print("PUT user:", request.user)
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
            print("DELETE user:", request.user)
            return super().delete(request, *args, **kwargs)
