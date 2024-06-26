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
    name = models.CharField(max_length=255, unique=True, validators=[RegexValidator(regex="^[a-zA-Z0-9 ]+$")])
    sugar = models.IntegerField()
    coffee = models.IntegerField()
    flour = models.IntegerField()
    chocolate = models.IntegerField()
    vertical = models.BinaryField()
    price = models.IntegerField()
    image = models.ImageField(upload_to='products/images/')


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True, unique=True)
    username = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    products = models.ManyToManyField(Product, through='Orders_Product')
    purchase_amount = models.IntegerField(validators=[MinValueValidator(0)])
    type = models.BooleanField()  # استفاده از بولین فیلد بجای باینری

class Orders_Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

class Storage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255, validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")], unique=True)
    amount = models.IntegerField()

class Users_Orders(models.Model):
    users_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)