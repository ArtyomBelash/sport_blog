from django.db import models
from django.urls import reverse


class CategoryShop(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория продукта')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('CategoryShop', on_delete=models.CASCADE)
    name_product = models.CharField(max_length=255, verbose_name='Имя продукта')
    slug = models.SlugField(max_length=255, db_index=True, unique=True)
    image = models.ImageField(upload_to='sport', blank=True, verbose_name='Картинка')
    descripion = models.TextField(verbose_name='Описание')
    price = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Цена')
    stock = models.PositiveIntegerField(verbose_name='Количество')
    available = models.BooleanField(default=True, verbose_name='Наличие')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        index_together = ('id', 'slug',)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name_product

    def get_absolute_url(self):
        return reverse('product', args=[self.slug])
