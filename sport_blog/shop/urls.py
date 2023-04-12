from django.urls import path, include
from .views import *

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('product/<slug:product_slug>/', ProductDetail.as_view(), name='product'),
    path('orders/', include('order1.urls')),
    path('category/<slug:slug>', CategoryShopView.as_view(), name='product_category')
]