from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.backends import ModelBackend
from django.forms import inlineformset_factory

    
class SignUpForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label=_('نام کامل'))
    phone_number = forms.CharField(max_length=13, label=_('شماره تلفن'))
    password1 = forms.CharField(
        label=_('رمز عبور'),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_('تکرار رمز عبور'),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'full_name', 'phone_number']
        labels = {
            'username': _('نام کاربری'),
            'email': _('ایمیل'),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            raise forms.ValidationError(_("استفاده از @ در نام کاربری غیر مجاز است"))
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if Users.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError(_("این شماره تلفن قبلاً ثبت شده است. لطفاً یک شماره دیگر استفاده کنید."))
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("این ایمیل قبلاً ثبت شده است. لطفاً یک ایمیل دیگر استفاده کنید."))
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save() 
        users = Users(
            user=user,
            full_name=self.cleaned_data['full_name'],
            phone_number=self.cleaned_data['phone_number'],
        )
        if commit:
            users.save()  
        return user 
    
class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label='Username or Email',
        max_length=150,
    )
    password = forms.CharField(
        label='Password',
    )
    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if not username_or_email or not password:
            raise forms.ValidationError('Both fields are required.')

        return cleaned_data
    
class AddStorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['name', 'amount']
        labels = {
            'name' : _('نام ماده اولیه'),
            'amount' : _('مقدار اولیه'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UpdateStorageForm(forms.ModelForm):
    class Meta:
        model = Storage
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
        
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'category']
        labels = {
            'name': _('نام محصول'),
            'price': _('قیمت'),
            'image': _('تصویر'),
            'category': _('دسته‌بندی'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['storage' , 'quantity']
        labels = {
            'storage': _('نام ماده اولیه'),
            'quantity': _('مقدار'),
        }
        widgets = {
            'storage': forms.Select(attrs={'class': 'form-control'}),
        }

# ایجاد فرم‌ست برای مواد اولیه
IngredientFormSet = inlineformset_factory(Product, Ingredient, form=IngredientForm, extra=3, can_delete=True)


class ChartForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all())
    start_date = forms.DateField(widget=forms.SelectDateWidget)
    end_date = forms.DateField(widget=forms.SelectDateWidget)