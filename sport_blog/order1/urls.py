from django.urls import path
from .views import *

urlpatterns = [
    path('create/', order_create, name='get_order'),
    # path('create/', OrderView.as_view(), name='get_order'),
]