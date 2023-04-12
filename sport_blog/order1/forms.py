from django import forms
from .models import Orders


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ('name', 'surname', 'phone', 'email', 'address')

# class OrderForm(forms.Form):
#     address = forms.CharField()
#     name = forms.CharField()
#     surname = forms.CharField()
#     phone = forms.CharField()
