from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST

from .forms import RegisterForm, OrderForm, ReviewForm
from .models import Dish, Order, OrderItem, Category, Review


def index(request):
    dishes = Dish.objects.all()[:5]
    return render(request, "restaurant_application/index.html", {"dishes": dishes})


def menu(request):
    category_id = request.GET.get("category")
    categories = Category.objects.all()

    if category_id:
        dishes = Dish.objects.filter(category_id=category_id)
    else:
        dishes = Dish.objects.all()

    return render(request, "restaurant_application/menu.html", {
        "dishes": dishes,
        "categories": categories,
        "selected_category": category_id,
    })


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


@login_required
def checkout(request):
    order = Order.objects.filter(user=request.user, is_paid=False).first()
    if not order or not order.items.exists():
        return redirect("cart")

    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = "new"
            order.is_paid = True
            order.save()
            return render(request, "restaurant_application/order_success.html", {"order": order})
    else:
        form = OrderForm(instance=order)

    return render(request, "restaurant_application/order.html", {"form": form, "order": order})


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, is_paid=True).order_by("-created_at")
    return render(request, "restaurant_application/order_history.html", {"orders": orders})


@login_required
def repeat_order(request, order_id):
    old_order = get_object_or_404(Order, id=order_id, user=request.user)

    new_order = Order.objects.create(
        user=request.user,
        full_name=old_order.full_name,
        phone=old_order.phone,
        address=old_order.address,
        payment_method=old_order.payment_method,
        status="new",
        is_paid=False,
    )

    for item in old_order.items.all():
        OrderItem.objects.create(
            order=new_order,
            dish=item.dish,
            quantity=item.quantity,
        )

    return redirect("cart")


def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = dish.reviews.all().order_by("-created_at")

    if request.method == "POST":
        # створення відгуку
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.dish = dish
                review.user = request.user
                review.save()
                return redirect("dish_detail", dish_id=dish.id)
        else:
            return redirect("login")
    else:
        form = ReviewForm()

    return render(request, "restaurant_application/dish_detail.html", {
        "dish": dish,
        "reviews": reviews,
        "form": form,
    })


@staff_member_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    dish_id = review.dish.id
    review.delete()
    return redirect("dish_detail", dish_id=dish_id)
