from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Категорія")

    def __str__(self):
        return self.name


class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категорія")
    description = models.TextField(verbose_name="Опис")
    ingredients = models.TextField(verbose_name="Інгредієнти")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Ціна")
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name="Зображення")
    available = models.BooleanField(default=True, verbose_name="Доступна")

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    def __str__(self):
        return f"Замовлення {self.id} від {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Замовлення")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Страва")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Кількість")

    def __str__(self):
        return f"{self.dish.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.dish.price * self.quantity


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Страва")
    rating = models.PositiveIntegerField(default=5, verbose_name="Оцінка")
    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.dish.name}"
