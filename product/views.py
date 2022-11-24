import datetime
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .models import User
from product.models import Product, ProductUser
from .shopee import Shopee
from .tiki import Tiki
from .feature_extract import FeatureExtract


# Create your views here.
def crawl_shopee(request):
  shopee_crawl = Shopee()
  shopee_crawl.crawl()
  return HttpResponseRedirect(reverse('homepage'))


def crawl_tiki(request):
  tiki_crawl = Tiki()
  tiki_crawl.crawl()
  return HttpResponseRedirect(reverse('homepage'))


def training(request):
  training = FeatureExtract()
  training.store()
  return HttpResponseRedirect(reverse('homepage'))


def search(request):
  filter_arr = []
  path = './static/upload/'
  file_name = 'anonymous'
  if request.method == 'GET':
    return HttpResponseRedirect(reverse('homepage'))
  if request.POST:
    search_image = request.FILES['img_file']
    if request.session.get('auth'):
      file_name = str(request.session.get('auth').get('id')) + '_file'
    handle_uploaded_file(search_image, file_name=file_name)
    obj = FeatureExtract()
    results = obj.search(search_image)
    for result in results:
      filter_arr.append(result[0])
  products = Product.objects.filter(original_id__in=filter_arr)
  template = loader.get_template('resultspage.html')
  context = {
    "products": products,
    "filters": filter_arr,
    "search_file": path + file_name + '.jpg'
  }
  return HttpResponse(template.render(context, request))


def recent(request):
  if not request.session.get('auth'):
    return HttpResponseRedirect(reverse('login'))
  user = User.objects.get(id=request.session.get('auth').get('id'))
  products = user.product_set.all().order_by('-productuser__view_date')
  paginator = Paginator(products, 8)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  context = {
    'products': page_obj,
  }
  template = loader.get_template('recentpage.html')
  return HttpResponse(template.render(context, request))


def destroy_recent(request, id):
  user_id = request.session.get('auth').get('id')
  recent = get_object_or_404(ProductUser, product=id, user=user_id)
  recent.delete()
  return HttpResponseRedirect(reverse('recent'))


def favorite(request):
  if not request.session.get('auth'):
    return HttpResponseRedirect(reverse('login'))
  user = User.objects.get(id=request.session.get('auth').get('id'))
  products = user.product_set.filter(productuser__favorite=True).order_by('-productuser__view_date')
  paginator = Paginator(products, 8)
  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)
  print(products)
  context = {
    'products': page_obj,
  }
  template = loader.get_template('favoritespage.html')
  return HttpResponse(template.render(context, request))


def add_favorite(request, id):
  if not request.session.get('auth'):
    return HttpResponseRedirect(reverse('login'))
  product = get_object_or_404(Product, id=id)
  if product:
    if request.session.get('auth'):
      user = User.objects.get(id=request.session.get('auth').get('id'))
      product_user = ProductUser.objects.filter(product=product, user=user)
      if not product_user:
        pivot = ProductUser(
          product=product,
          user=user,
          favorite=True,
        )
        pivot.save()
        return JsonResponse({}, status=200)
      elif product_user[0].favorite:
        product_user.update(favorite=False)
        return JsonResponse({}, status=400)
      else:
        product_user.update(favorite=True)
        return JsonResponse({}, status=200)
  return JsonResponse({}, status=401)


def go_to_link(request, id):
  product = get_object_or_404(Product, id=id)
  if product:
    if request.session.get('auth'):
      user = User.objects.get(id=request.session.get('auth').get('id'))
      product_user = ProductUser.objects.filter(product=product, user=user)
      if not product_user:
        pivot = ProductUser(
          product=product,
          user=user,
        )
        pivot.save()
      else:
        product_user.update(view_date=datetime.datetime.now())
    return HttpResponseRedirect(product.product_link)
  return HttpResponseRedirect('homepage')


def handle_uploaded_file(f, file_name):
  with open('./static/upload/' + file_name + '.jpg', 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)
