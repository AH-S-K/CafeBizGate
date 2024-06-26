from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Users, Orders, Orders_Product, Storage, Admins
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse


def index(request):
    best_selling_products = Product.objects.all()[:12]
    return render(request, 'index.html', {'best_selling_products': best_selling_products})


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            if username_or_email=="admin" and password=='admin':
                user = authenticate(request, username=username_or_email , password=password)
                login(request, user)
                return redirect('management')
            if "@" not in username_or_email:
                user = authenticate(request, username=username_or_email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است')
            else :
                username = User.objects.filter(email = username_or_email).first()
                user = authenticate(request , username= username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index')
                else:
                    form.add_error(None, 'ایمیل یا رمز عبور اشتباه است')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')

def is_admin(user):
    return user.username == 'admin'
