from django.urls import path
from . import views

urlpatterns = [
  path('shopee/', views.crawl_shopee, name='shopeeCrawl'),
  path('tiki/', views.crawl_tiki, name='tikiCrawl'),
  path('train/', views.training, name='training'),
  path('search/', views.search, name='search'),
  path('recent/', views.recent, name='recent'),
  path('favorite/', views.favorite, name='favorite'),
  path('product/<int:id>', views.go_to_link, name='to_product'),
]
