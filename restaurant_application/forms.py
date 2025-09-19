from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Order, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"})
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})
            if field_name == "username":
                field.widget.attrs["placeholder"] = "Username"
            elif field_name == "password1":
                field.widget.attrs["placeholder"] = "Пароль"
            elif field_name == "password2":
                field.widget.attrs["placeholder"] = "Підтвердження пароля"


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
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Ваш відгук..."}),
            "rating": forms.Select(attrs={"class": "form-select"}),
        }
        labels = {
            "comment": "Відгук",
            "rating": "Оцінка (1-5)",
        }
