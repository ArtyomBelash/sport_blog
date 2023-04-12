from django.urls import path, include
from .views import *


urlpatterns = [
    path('', cart_detail, name='cart_detail'),
    path('remove/<slug:slug>/', cart_remove, name='cart_remove'),
    path('add/<slug:slug>/', cart_add, name='cart_add'),
]