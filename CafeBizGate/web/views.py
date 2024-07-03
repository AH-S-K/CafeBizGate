from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Product, Users, Orders, Orders_Product, Storage, Admins
from .forms import *
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy , reverse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.db import transaction
from django.db.models import Sum , Count ,F
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDay , TruncMonth , TruncWeek


def index(request):
    best_selling_products = Product.objects.annotate(
    total_sales=Sum('orders_product__quantity')
    ).order_by('-total_sales')[:12]

    context = {
        'best_selling_products': best_selling_products,
    }

    return render(request, 'index.html', context)

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
            if username_or_email=="admin":
                try :
                    user = authenticate(request, username=username_or_email , password=password)
                    login(request, user)
                    return redirect('management')
                except Exception:
                    form.add_error(None, 'نام کاربری یا رمز عبور اشتباه است')
                    
            elif "@" not in username_or_email:
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

def sales_data(request):
    product_id = request.GET.get('product_id')
    period = request.GET.get('period')  # 'daily', 'weekly', 'monthly'

    end_date = timezone.now()

    if period == 'daily':
        start_date = end_date - timedelta(days=30)
        Trunc_function = TruncDay
    elif period == 'weekly':
        start_date = end_date - timedelta(weeks=12)  # حدودا 3 ماه
        Trunc_function = TruncWeek
    elif period == 'monthly':
        start_date = end_date - timedelta(days=365)
        Trunc_function = TruncMonth
    else:
        return JsonResponse({'error': 'Invalid period'}, status=400)
    
    
    sales_data = Orders_Product.objects.filter(
        orders_order_id__order_date__range=[start_date, end_date],
        product_id=product_id
    ).annotate(
        period=Trunc_function('orders_order_id__order_date')
    ).values(
        'period'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('period')
    
    
    sales_data_list = list(sales_data)
    
    return JsonResponse(sales_data_list, safe=False)

@login_required(login_url='login')
@transaction.atomic
def add_to_cart(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        
        # اضافه کردن محصول به سبد خرید
        user_order, created = Orders.objects.get_or_create(username=request.user.custom_user, type=False , defaults={'order_date': timezone.now()})
        
        # محاسبه مقدار مورد نیاز هر ماده اولیه برای محصول جدید
        required_ingredients = {}
        for ingredient in product.ingredients.all():
            if ingredient.storage.id not in required_ingredients:
                required_ingredients[ingredient.storage.id] = 0
            required_ingredients[ingredient.storage.id] += ingredient.quantity
        
        # محاسبه مقدار مورد نیاز برای محصولات فعلی در سبد خرید
        for order_item in user_order.orders_product_set.all():
            for ingredient in order_item.product_id.ingredients.all():
                if ingredient.storage.id not in required_ingredients:
                    required_ingredients[ingredient.storage.id] = 0
                required_ingredients[ingredient.storage.id] += order_item.quantity * ingredient.quantity
        
        # بررسی موجودی انبار
        insufficient_ingredients = []
        for storage_id, required_amount in required_ingredients.items():
            storage = Storage.objects.select_for_update().get(id=storage_id)
            if storage.amount < required_amount:
                insufficient_ingredients.append(storage.name)
        
        if insufficient_ingredients:
            return JsonResponse({'error': 'موجودی کافی نیست!'}, status=400)
        
        # در صورتی که موجودی کافی باشد، محصول به سبد خرید اضافه می‌شود
        order_product, created = Orders_Product.objects.get_or_create(orders_order_id=user_order, product_id=product)
        
        if not created:
            order_product.quantity += 1
        order_product.save()
        
        # به روزرسانی purchase_amount
        user_order.purchase_amount += product.price
        user_order.save()
        
        return JsonResponse({'success': 'محصول با موفقیت به سبد خرید اضافه شد!'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='login')
@transaction.atomic
def cart(request):
    user_orders = Orders.objects.filter(username=request.user.custom_user, type=False)
    user_order = user_orders[0] if user_orders.exists() else None

    if request.method == 'POST':
        if 'update_quantity' in request.POST:
            product_id = request.POST.get('product_id')
            new_quantity = int(request.POST.get('quantity'))
            order_product = Orders_Product.objects.get(orders_order_id=user_order, product_id=product_id)
            
            required_ingredients = {}
            for ingredient in order_product.product_id.ingredients.all():
                if ingredient.storage.id not in required_ingredients:
                    required_ingredients[ingredient.storage.id] = 0
                required_ingredients[ingredient.storage.id] += (new_quantity - order_product.quantity) * ingredient.quantity

            insufficient_ingredients = []
            for storage_id, required_amount in required_ingredients.items():
                storage = Storage.objects.get(id=storage_id)
                if storage.amount < required_amount:
                    insufficient_ingredients.append(storage.name)

            if insufficient_ingredients:
                return JsonResponse({'error': 'موجودی کافی نیست!'}, status=400)

            user_order.purchase_amount += (new_quantity - order_product.quantity) * order_product.product_id.price
            order_product.quantity = new_quantity
            order_product.save()
            user_order.save()
            return JsonResponse({'success': "تعداد محصول با موفقیت بروزرسانی شد!"})

        elif 'place_order' in request.POST:
            order_type = request.POST.get('order_type') == 'on'

            if not user_order:
                return JsonResponse({'error': 'سبد خرید فعال یافت نشد.'}, status=400)

            required_ingredients = {}
            for order_product in user_order.orders_product_set.all():
                product = order_product.product_id
                for ingredient in product.ingredients.all():
                    if ingredient.storage.id not in required_ingredients:
                        required_ingredients[ingredient.storage.id] = 0
                    required_ingredients[ingredient.storage.id] += order_product.quantity * ingredient.quantity

            insufficient_ingredients = []
            for storage_id, required_amount in required_ingredients.items():
                storage = Storage.objects.get(id=storage_id)
                if storage.amount < required_amount:
                    insufficient_ingredients.append(storage.name)

            if insufficient_ingredients:
                return JsonResponse({'error': 'موجودی کافی نیست!'}, status=400)

            for storage_id, required_amount in required_ingredients.items():
                storage = Storage.objects.get(id=storage_id)
                storage.amount -= required_amount
                storage.save()

            total_amount = sum(item.product_id.price * item.quantity for item in user_order.orders_product_set.all())
            user_order.purchase_amount = total_amount
            user_order.type = True
            user_order.order_date = timezone.now()
            user_order.save()

            return JsonResponse({'success': 'سفارش با موفقیت ثبت شد!', 'redirect_url': reverse('order_summary', args=[user_order.order_id])})

    context = {
        'cart_items': user_order.orders_product_set.all() if user_order else [],
    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
@transaction.atomic
def remove_from_cart(request, product_id):
    if request.method == 'POST':
        user_order = Orders.objects.get(username=request.user.custom_user, type=False)
        order_product = get_object_or_404(Orders_Product, orders_order_id=user_order, product_id=product_id)

        # به روزرسانی purchase_amount
        user_order.purchase_amount -= order_product.product_id.price * order_product.quantity

        order_product.delete()
        # JsonResponse({'success': "محصول با موفقیت حذف شد!"})
        # اگر هیچ محصولی در سبد خرید باقی نماند، سفارش را نیز حذف کن
        if user_order.orders_product_set.count() == 0:
            user_order.delete()
        else:
            user_order.save()

        return redirect('cart')
    return JsonResponse({'error': 'Invalid request method'}, status=400)


@login_required(login_url='login')
def order_summary(request, order_id):
    order = Orders.objects.get(order_id=order_id)
    context = {
        'order': order,
        'order_items': order.orders_product_set.all(),
    }
    return render(request, 'order_summary.html', context)


@login_required(login_url='login')
def order_history(request):
    completed_orders = Orders.objects.filter(username=request.user.custom_user, type=True)
    orders_info = []
    for order in completed_orders:
        order_products = order.orders_product_set.all()
        products_info = []
        for order_product in order_products:
            product = order_product.product_id
            total_price = product.price * order_product.quantity
            products_info.append({
                'product_name': product.name,
                'product_image': product.image.url,
                'product_price': product.price,
                'quantity': order_product.quantity,
                'total_price': total_price,
            })
        orders_info.append({
            'order_id': order.order_id,
            'purchase_amount': order.purchase_amount,
            'products_info': products_info,
        })
    context = {
        'orders_info': orders_info,
    }
    return render(request, 'order_history.html', context)


@login_required(login_url='login')
def clear_cart(request):
    # دریافت همه‌ی سفارشات کاربر
    user_orders = Orders.objects.filter(username=request.user.custom_user, type=False)
    
    # حذف همه‌ی سفارشات
    user_orders.delete()
    
    # پیام موفقیت‌آمیز برای کاربر
    messages.success(request, 'Your cart has been cleared successfully!')
    
    # ریدایرکت به صفحه‌ای دیگر، به عنوان مثال به صفحه‌ی اصلی یا همان صفحه‌ی سبد خرید
    return redirect('cart')


def clear_purchase_history(request):
    if request.method == 'POST':
        Orders_Product.objects.all().delete()
        Users_Orders.objects.all().delete()
        Orders.objects.all().delete()
        messages.success(request, 'Purchase history has been cleared.')
        return redirect('clear_purchase_history')
    return render(request, 'clear_purchase_history.html')