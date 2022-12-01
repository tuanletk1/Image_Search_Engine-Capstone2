from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('register/', views.register, name='register'),
  path('user/', views.users, name='user'),
  path('mod/', views.mods, name='mod'),
  path('', views.homepage, name='homepage'),
  path('update_role/', views.update_role, name='update_role'),
  path('remove_account/', views.remove_account, name='remove_account'),
  path('crawl/', views.crawl, name='crawl')
]
