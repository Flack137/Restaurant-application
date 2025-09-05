from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "payment_method"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ваше ПІБ"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Телефон"}),
            "address": forms.Textarea(attrs={"class": "form-control", "placeholder": "Адреса доставки", "rows": 3}),
            "payment_method": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "full_name": "ПІБ",
            "phone": "Телефон",
            "address": "Адреса доставки",
            "payment_method": "Метод оплати",
        }