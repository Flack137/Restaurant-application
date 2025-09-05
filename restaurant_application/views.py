from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Dish, Order, OrderItem


def index(request):
    dishes = Dish.objects.all()[:5]
    return render(request, "restaurant_application/index.html", {"dishes": dishes})


def menu(request):
    dishes = Dish.objects.all()
    return render(request, "restaurant_application/menu.html", {"dishes": dishes})


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()
    return render(request, "restaurant_application/register.html", {"form": form})


@login_required
def profile(request):
    return render(request, "restaurant_application/profile.html")


def custom_logout(request):
    logout(request)
    return redirect('/')


# === CART ===

@login_required
def add_to_cart(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    order, created = Order.objects.get_or_create(user=request.user, is_paid=False)
    item, item_created = OrderItem.objects.get_or_create(order=order, dish=dish)
    if not item_created:
        item.quantity += 1
        item.save()
    return redirect("cart")


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_paid=False)
    item.delete()
    return redirect("cart")


@login_required
def update_quantity(request, item_id):
    item = get_object_or_404(OrderItem, id=item_id, order__user=request.user, order__is_paid=False)
    if request.method == "POST":
        quantity = int(request.POST.get("quantity", 1))
        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()
    return redirect("cart")


@login_required
def cart_view(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    return render(request, "restaurant_application/cart.html", {"order": order})
