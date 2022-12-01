from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse

from . import forms
from .models import User, Permission
from product.models import Product, ProductUser


# Create your views here.
def login(request):
    if request.session.get('auth'):
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST['email'])
            if check_password(request.POST['password'], user.password):
                set_session(request=request, user=user)
                return HttpResponseRedirect(reverse('homepage'))
    else:
        form = forms.LoginForm()
    context = {
        'form': form,
    }
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


def register(request):
    if request.session.get('auth'):
        return HttpResponseRedirect(reverse('homepage'))
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            user = User(
                username=username,
                email=email,
                password=make_password(password),
                avatar='../../static/assets/images/cat.jpg'
            )
            user.save()
            permission = Permission.objects.get(id=4)
            permission.users.add(user)
            print(user)
            set_session(request=request, user=user)
            return HttpResponseRedirect(reverse('homepage'))
    else:
        form = forms.RegisterForm()
    context = {
        'form': form,
    }
    template = loader.get_template('register.html')
    return HttpResponse(template.render(context, request))


def logout(request):
    try:
        del request.session['auth']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('homepage'))


def homepage(request):
    if request.session.get('auth'):
        template = loader.get_template('homepage.html')

    else:
        template = loader.get_template('subhomepage.html')
    products = Product.objects.all().values()
    paginator = Paginator(products, 20)
    page_obj = paginator.get_page(1)
    context = {
        'products': page_obj,
    }
    return HttpResponse(template.render(context, request))


def users(request):
    users = User.objects.filter(Q(permission__permission='user'))
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    template = loader.get_template('usermanagementpage.html')
    return HttpResponse(template.render(context, request))


def mods(request):
    mods = User.objects.filter(Q(permission__permission__contains='mod'))
    paginator = Paginator(mods, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    template = loader.get_template('modmanagmentpage.html')
    return HttpResponse(template.render(context, request))


def update_role(request):
    if request.method == 'POST':
        user = get_object_or_404(User, id=request.POST['edit_id'])
        user.permission_set.set([request.POST['edit_role']])
        return JsonResponse({}, status=200)
    return JsonResponse({}, status=400)


def remove_account(request):
    if request.method == 'POST':
        account = get_object_or_404(User, id=request.POST['remove_id'])
        account.delete()
        return JsonResponse({}, status=200)
    return JsonResponse({}, status=400)


def crawl(request):
    products = Product.objects.all().order_by('ctime')
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    template = loader.get_template('moddashboard.html')
    return HttpResponse(template.render(context, request))


def set_session(request, user):
    request.session['auth'] = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active,
        'avatar': user.avatar,
        'permission': user.permission_set.all().values().get().get('permission')
    }
