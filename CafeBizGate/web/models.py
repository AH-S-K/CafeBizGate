from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator, EmailValidator

class Users(models.Model):
    username = models.CharField(max_length=255, primary_key=True, unique=True,validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")])
    full_name = models.CharField(max_length=255, validators=[RegexValidator(regex="^[a-zA-Z ]+$")])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255, unique=True,validators=[MinLengthValidator(8)])
    phone_number = models.IntegerField(validators=[RegexValidator(r'^\d{11}$' , 'Phone number must be 11 digits' , 'Invalid number')],unique=True)
class Admins(models.Model):
    username = models.CharField(max_length=255, unique=True,primary_key=True, validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255 , unique=True)

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True , unique=True)
    username = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    products = models.CharField(max_length=255)
    purchase_amount = models.IntegerField(validators=[MinValueValidator(0)])
    type = models.BooleanField() #از بولین فیلد استفاده کردم بجای باینری

class Product(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    name = models.CharField(max_length=255 , unique=True)
    sugar = models.IntegerField()
    coffee = models.IntegerField()
    flour = models.IntegerField()
    chocolate = models.IntegerField()
    vertical = models.BinaryField()
    price = models.IntegerField()

class Orders_Product(models.Model):
    id = models.AutoField(primary_key=True , unique=True)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)

class Storage(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()

class Users_Orders(models.Model):
    users_username = models.ForeignKey(Users, on_delete=models.CASCADE)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)