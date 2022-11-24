from django.urls import path
from . import views

urlpatterns = [
  path('shopee/', views.crawl_shopee, name='shopeeCrawl'),
  path('tiki/', views.crawl_tiki, name='tikiCrawl'),
  path('train/', views.training, name='training'),
  path('search/', views.search, name='search'),
  path('recent/', views.recent, name='recent'),
  path('recent/delete/<int:id>', views.destroy_recent, name='delete_recent'),
  path('favorite/', views.favorite, name='favorite'),
  path('add_favorite/<int:id>', views.add_favorite, name='add_favorite'),
  path('product/<int:id>', views.go_to_link, name='to_product'),
]
