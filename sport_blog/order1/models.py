from django.core.validators import RegexValidator
from django.db import models
from cart.cart import Cart
from phonenumber_field.modelfields import PhoneNumberField

from shop.models import Product


class Orders(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    phone = PhoneNumberField(region='BY', verbose_name='Телефон')
    email = models.EmailField(default=None)
    address = models.CharField(max_length=600, verbose_name='Адрес')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обнавлено')
    paid = models.BooleanField(default=False, verbose_name='Заплачено')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.pk}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Orders, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items1', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.pk}'

    def get_cost(self):
        return self.price * self.quantity

