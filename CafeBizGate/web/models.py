from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, EmailValidator
from django.contrib.auth.models import User

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='custom_user')
    full_name = models.CharField(max_length=255, validators=[RegexValidator(regex="^[a-zA-Z ]+$")])
    phone_number = models.CharField(max_length=13, validators=[RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in the format 09xx_xxx_xxxx', code='invalid_phone_number')], unique=True)

class Admins(models.Model):
    username = models.CharField(max_length=255, unique=True, primary_key=True, validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(8)])


class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, unique=True, validators=[RegexValidator(regex="^[a-zA-Z0-9آ-ی ]+$")])
    price = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    COLD_DRINK = 'CD'
    HOT_DRINK = 'HD'
    TEA = 'TI'
    CAKE = 'CK'
    CATEGORY_CHOICES = [
        (COLD_DRINK, 'نوشیدنی سرد'),
        (HOT_DRINK, 'نوشیدنی گرم'),
        (TEA, 'چای و دمنوش'),
        (CAKE, 'کیک'),
    ]
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=CAKE)
    def __str__(self):
        return self.name



class Orders(models.Model):
    order_id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='Orders_Product')
    purchase_amount = models.IntegerField(validators=[MinValueValidator(0)] , default=0)
    type = models.BooleanField(default=False)  # استفاده از بولین فیلد بجای باینری
    order_date = models.DateTimeField()  # افزودن فیلد تاریخ
    TAKEAWAY = 'TA'
    INSTORE = 'IS'
    PURCHASE_TYPE_CHOICES = [
        (TAKEAWAY, 'Takeaway'),
        (INSTORE, 'Instore'),
    ]
    purchase_type = models.CharField(max_length=2, choices=PURCHASE_TYPE_CHOICES, default=TAKEAWAY)

    
class Orders_Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1) 


class Storage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, validators=[RegexValidator(regex="^[a-zA-Z0-9آ-ی ]+$")], unique=True)
    amount = models.IntegerField(validators=[MinValueValidator(0)])
    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='ingredients')
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name} - {self.storage.name} - {self.quantity}"
    
class Users_Orders(models.Model):
    users_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)