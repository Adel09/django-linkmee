from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.loginuser, name='test'),
    path('register', views.registeruser, name='register'),
    path('mylinks', views.getMyLinks, name='api-links'),
    path('my-page', views.getMyPage, name='api-page'),
    path('user', views.getUser, name='api-user'),
]