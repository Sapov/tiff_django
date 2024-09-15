from django import forms

from delivery_in_bus.models import OrdersDeliveryBus


class FormLoadImg(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = '__all__'
