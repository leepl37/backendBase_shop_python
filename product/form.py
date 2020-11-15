from product.models import Product, Order
from django import forms



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']