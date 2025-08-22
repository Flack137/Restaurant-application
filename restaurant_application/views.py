from django.shortcuts import render
from .models import Dish, Category

def index(request):
    popular_dishes = Dish.objects.filter(available=True)[:5]  # 5 популярных (для примера)
    return render(request, 'index.html', {'popular_dishes': popular_dishes})

def menu(request):
    categories = Category.objects.all()
    dishes = Dish.objects.filter(available=True)
    return render(request, 'menu.html', {'categories': categories, 'dishes': dishes})
