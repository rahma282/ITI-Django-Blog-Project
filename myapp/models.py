from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.user.first_name
    

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    author =  models.ForeignKey(Author,on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comments(models.Model):
    content = models.TextField()
    created_by = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='comments')
    post =  models.ForeignKey(Post,on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    