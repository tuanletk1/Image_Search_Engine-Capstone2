from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.db.models import Q
from django.core.paginator import Paginator

from . import forms
from .models import User, Permission
from product.models import Product


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
    users = User.objects.filter(~Q(permission__permission='admin') | Q(permission__permission__contains='mod'))
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj
    }
    template = loader.get_template('usermanagementpage.html')
    return HttpResponse(template.render(context, request))


def set_session(request, user):
    request.session['auth'] = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active,
        'permission': user.permission_set.all().values().get().get('permission')
    }
