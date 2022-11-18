from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('user/', views.users, name='user'),
  path('', views.homepage, name='homepage'),
]
