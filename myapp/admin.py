from django.contrib import admin
from .models import Post, Author, Comments

# Register your models here.
admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comments)

