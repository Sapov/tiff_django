from django import forms
from .models import *


class FormsOrderItem(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', "product", 'price_per_item', 'quantity', 'total_price', 'is_active']
