from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Dish

# Головна сторінка
def index(request):
    dishes = Dish.objects.all()[:5]  # популярні страви
    return render(request, "restaurant_application/index.html", {"dishes": dishes})


# Сторінка меню
def menu(request):
    dishes = Dish.objects.all()
    return render(request, "restaurant_application/menu.html", {"dishes": dishes})


# Реєстрація
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматичний вхід після реєстрації
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "restaurant_application/register.html", {"form": form})


# Профіль користувача
@login_required
def profile(request):
    return render(request, "restaurant_application/profile.html")


# Кастомний вихід (логаут)
def custom_logout(request):
    # Беремо адресу сторінки, з якої юзер натиснув "Вийти"
    next_url = request.META.get("HTTP_REFERER", "/")
    logout(request)
    return redirect(next_url)

def custom_logout(request):
    logout(request)
    return redirect('/')