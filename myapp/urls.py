from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import RegisterView, check_email, APILoginView 

urlpatterns = [

    # API views
    path('api/posts/', views.PostList.as_view(), name='post-list-create'),
    path('api/posts/<int:pk>/', views.PostDetails.as_view(), name='post-detail'),

    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', APILoginView.as_view(), name='api-login'), 

    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('api/check-email/', check_email, name='check-email'),
    
]
