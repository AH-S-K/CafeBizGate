from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Users, Admins, Orders, Product, Orders_Product, Storage, Users_Orders
from .forms import UserForm, OrderForm, ProductForm

# User Registration View
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

# User Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid login details.")
    return render(request, 'login.html')

# User Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Home View
@login_required
def home(request):
    return render(request, 'home.html')

# List Products View
@login_required
def list_products(request):
    products = Product.objects.all()
    return render(request, 'list_products.html', {'products': products})

# Create Product View
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_products')
    else:
        form = ProductForm()
    return render(request, 'create_product.html', {'form': form})

# Create Order View
@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.username = request.user
            order.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = OrderForm()
    return render(request, 'create_order.html', {'form': form})

# View Order Details
@login_required
def view_order(request, order_id):
    order = get_object_or_404(Orders, pk=order_id)
    return render(request, 'view_order.html', {'order': order})

# View User Orders
@login_required
def user_orders(request):
    orders = Orders.objects.filter(username=request.user)
    return render(request, 'user_orders.html', {'orders': orders})