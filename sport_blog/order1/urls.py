from django.urls import path
from .views import *

urlpatterns = [
    path('create/', order_create, name='get_order'),
]