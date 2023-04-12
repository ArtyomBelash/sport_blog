from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import *


#
# class OrderAdmin(admin.ModelAdmin):
#     raw_id_fields = ['product']

class OrderAdmin(TabularInline):
    model = OrderItem
    raw_id_fields = ['products', ]


admin.site.register(OrderItem)


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'phone', 'address', 'created', 'paid']
    list_editable = ['paid']


admin.site.register(Orders, OrdersAdmin)
