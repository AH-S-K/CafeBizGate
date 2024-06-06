from django import forms
from .models import Users , Orders , Product

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'full_name', 'email', 'password', 'phone_number']
        widgets = {
            'password': forms.PasswordInput(),
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['products', 'purchase_amount', 'type']
        widgets = {
            'products': forms.CheckboxSelectMultiple(),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'sugar', 'coffee', 'flour', 'chocolate', 'vertical', 'price']
