from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu/', views.menu, name='menu'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.custom_logout, name='logout'),
    path('cart/', views.cart_view, name="cart"),
    path('cart/add/<int:dish_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('cart/update/<int:item_id>/', views.update_quantity, name="update_quantity"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/history/", views.order_history, name="order_history"),
    path("orders/repeat/<int:order_id>/", views.repeat_order, name="repeat_order"),
    path("dish/<int:dish_id>/", views.dish_detail, name="dish_detail"),
    path("review/delete/<int:review_id>/", views.delete_review, name="delete_review"),
]
