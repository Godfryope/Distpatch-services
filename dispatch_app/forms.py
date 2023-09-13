from django import forms
from .models import Product

class OrderForm(forms.Form):
    customer_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Select a product")
    quantity = forms.IntegerField(min_value=1)
