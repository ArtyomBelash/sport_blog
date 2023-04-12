from django.shortcuts import render
from django.views.generic import FormView, DetailView

from .forms import *
from .models import *
from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # order = form
            # order.save()
            new_order = Orders.objects.create(name=form.cleaned_data.get('name'),
                                              surname=form.cleaned_data.get('surname'),
                                              phone=form.cleaned_data.get('phone'),
                                              email=form.cleaned_data.get('email'),
                                              address=form.cleaned_data.get('address'))
            # order = Orders.objects.get(phone=request.POST.get('phone'))
            order = Orders.objects.get(pk=new_order.pk)
            for i in cart:
                OrderItem.objects.create(order=order,
                                         product=i['product'],
                                         price=i['price'],
                                         quantity=i['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders1/ty.html',
                          {'order': order})
    else:
        form = OrderForm()
    return render(request, 'orders1/detail_order.html',
                  {'cart': cart, 'form': form})
