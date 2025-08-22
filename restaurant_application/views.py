from django.shortcuts import render
from .models import Dish

def index(request):
    return render(request, 'restaurant_application/index.html')

def menu(request):
    dishes = Dish.objects.all()
    return render(request, 'restaurant_application/menu.html', {'dishes': dishes})
