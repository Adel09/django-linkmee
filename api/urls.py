from django.urls import path, include
from . import views

urlpatterns = [
    path('login', views.loginuser, name='test'),
    path('register', views.registeruser, name='register'),
    path('mylinks', views.getMyLinks, name='api-links'),
    path('my-page', views.getMyPage, name='api-page'),
    path('user', views.getUser, name='api-user'),
    path('links/add', views.addLink, name='api-addlink'),
    path('user/update-bio', views.updatebio, name="api-update-user-bio")
]