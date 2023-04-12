from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from .models import *
from cart.forms import CartAddProductForm


class ProductView(ListView):
    model = Product
    context_object_name = 'products'
    ordering = ['-updated']
    paginate_by = 6
    template_name = 'shop/all_products.html'
    queryset = Product.objects.filter(available=True)


class ProductDetail(DetailView, FormView):
    form_class = CartAddProductForm
    model = Product
    context_object_name = 'product'
    ordering = ['-updated']
    template_name = 'shop/product_detail.html'
    slug_url_kwarg = 'product_slug'


class CategoryShopView(ListView):
    model = Product
    context_object_name = 'product_category'
    ordering = ['-updated']
    paginate_by = 6
    template_name = 'shop/product_category.html'

    def get_queryset(self):
        cat = CategoryShop.objects.get(slug=self.kwargs['slug'])
        return super().get_queryset().filter(category=cat)
