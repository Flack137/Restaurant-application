from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Review


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "rating"]
        widgets = {
            "comment": forms.Textarea(attrs={"rows": 3, "placeholder": "Ваш відгук..."}),
            "rating": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "comment": "Відгук",
            "rating": "Оцінка (1-5)",
        }
