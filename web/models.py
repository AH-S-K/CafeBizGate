
from django.db import models
from django.core.validators import RegexValidator,MinLengthValidator,MinValueValidator,EmailValidator



class User(models.Model):
    username = models.CharField(max_length=255, primary_key=True,validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")])
    full_name = models.CharField(max_length=255, validators=[RegexValidator(regex="^[a-zA-Z ]+$")])
    email = models.EmailField(max_length=255, unique=True , validators=[EmailValidator()])
    password = models.CharField(max_length=255 , validators=[MinLengthValidator(8)])
    phone_number = models.IntegerField()


class Admin(models.Model):
    username = models.CharField(max_length=255, primary_key=True ,validators=[RegexValidator(regex="^[a-zA-Z0-9_]+$")])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator()])
    password = models.CharField(max_length=255)


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE , null=True)
    products = models.CharField(max_length=255)
    purchase_amount = models.IntegerField()
    type = models.BooleanField()


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sugar = models.IntegerField()
    coffee = models.IntegerField()
    flour = models.IntegerField()
    chocolate = models.IntegerField()
    vertical = models.BinaryField()
    price = models.IntegerField()
    
    
class Orders_Product(models.Model):
    id = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Storage(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    amount = models.IntegerField()


class User_Orders(models.Model):
    users_username = models.ForeignKey(User, on_delete=models.CASCADE)
    orders_order_id = models.ForeignKey(Orders, on_delete=models.CASCADE)
