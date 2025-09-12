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

    @property
    def average_rating(self):
        """Повертає середній рейтинг (округлений до 1 знаку) або None, якщо відгуків немає."""
        reviews = self.reviews.all()
        if reviews.exists():
            avg = sum(r.rating for r in reviews) / reviews.count()
            return round(avg, 1)
        return None


class Order(models.Model):
    PAYMENT_METHODS = [
        ("card", "Онлайн карткою"),
        ("cash", "Готівка при отриманні"),
    ]

    STATUS_CHOICES = [
        ("new", "Нове"),
        ("paid", "Оплачене"),
        ("completed", "Виконане"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")

    full_name = models.CharField(max_length=200, verbose_name="ПІБ")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    address = models.TextField(verbose_name="Адреса доставки")
    payment_method = models.CharField(
        max_length=10, choices=PAYMENT_METHODS, default="cash", verbose_name="Метод оплати"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="new", verbose_name="Статус замовлення"
    )

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    @property
    def total_price(self):
        return sum(item.dish.price * item.quantity for item in self.items.all())


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
    # related_name='reviews' щоб зручно робити dish.reviews.all()
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name="Страва", related_name='reviews')
    rating = models.PositiveIntegerField(default=5, verbose_name="Оцінка")
    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Створено")

    def __str__(self):
        return f"Відгук від {self.user.username} на {self.dish.name}"
