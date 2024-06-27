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

def unauthorized_access(request):
    return render(request, 'unauthorized_access.html')

@user_passes_test(is_admin, login_url='/unauthorized/')
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@user_passes_test(is_admin, login_url='/unauthorized/')
def delete_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            print(username)
            user.delete()
            return redirect('user-list')
        except User.DoesNotExist:
            pass
    return redirect('user-list')

@user_passes_test(is_admin, login_url='/unauthorized/')
def delete_user2(request):
    try:
        user = User.objects.get(username='a2')
        user.delete()
        return redirect("login")
    except Users.DoesNotExist:
        return HttpResponse('User not found')

@user_passes_test(is_admin, login_url='/unauthorized/')
def management_view(request):
        return render(request, 'management.html')

@user_passes_test(is_admin, login_url='/unauthorized/')
def manage_inventory(request):
    add_form = AddStorageForm()
    update_form = UpdateStorageForm()
    
    if request.method == 'POST':
        if 'add_storage' in request.POST:
            add_form = AddStorageForm(request.POST)
            if add_form.is_valid():
                add_form.save()
                return redirect('manage_inventory')
        elif 'update_storage' in request.POST:
            storage_id = request.POST.get('storage_id')
            storage = get_object_or_404(Storage, id=storage_id)
            update_form = UpdateStorageForm(request.POST, instance=storage)
            if update_form.is_valid():
                update_form.save()
                return redirect('manage_inventory')
        elif 'delete_storage' in request.POST:
            storage_id = request.POST.get('storage_id')
            storage = get_object_or_404(Storage, id=storage_id)
            storage.delete()
            return redirect('manage_inventory')

    storages = Storage.objects.all()

    return render(request, 'manage_inventory.html', {
        'add_form': add_form,
        'update_form': update_form,
        'storages': storages,
    })

@user_passes_test(is_admin, login_url='/unauthorized/')
def add_product(request):
    product = None
    if 'edit' in request.GET:
        product = get_object_or_404(Product, id=request.GET.get('edit'))

    if request.method == 'POST':
        # Check if delete button was clicked
        if 'delete' in request.POST:
            product_id = request.POST.get('delete')
            product_to_delete = get_object_or_404(Product, id=product_id)
            product_to_delete.delete()
            return redirect('add_product')

        # Handle adding/editing product
        if product:
            product_form = ProductForm(request.POST, request.FILES, instance=product)
            ingredient_formset = IngredientFormSet(request.POST, instance=product)
        else:
            product_form = ProductForm(request.POST, request.FILES)
            ingredient_formset = IngredientFormSet(request.POST)

        if product_form.is_valid() and ingredient_formset.is_valid():
            saved_product = product_form.save()
            ingredient_formset.instance = saved_product
            ingredient_formset.save()
            return redirect('add_product')
    else:
        if product:
            product_form = ProductForm(instance=product)
            ingredient_formset = IngredientFormSet(instance=product)
        else:
            product_form = ProductForm()
            ingredient_formset = IngredientFormSet()

    products = Product.objects.all()
    return render(request, 'add_product.html', {
        'product_form': product_form,
        'ingredient_formset': ingredient_formset,
        'products': products,
        'product': product,
    })
