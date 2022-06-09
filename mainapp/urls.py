from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('account/register', views.signupuser, name='signupuser'),
    path('account/login', views.signinuser, name='signinuser'),
    path('account/logout', views.logoutuser, name='logoutuser'),
    path('account/dashboard', views.dashboard, name='dashboard'),
    path('account/dashboard/add-link', views.addlink, name='add-link'),
    path('test', views.testpage, name='test'),
    #path('app/api', views.allLinks, name='alllinks'),
    path('<str:username>', views.viewpage, name='viewpage'),
    path('delete/<str:id>', views.delete, name='delete'),
    
    
]
