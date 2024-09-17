from django import forms

from delivery_in_bus.models import OrdersDeliveryBus


class FormLoadImg(forms.ModelForm):
    # order_id =
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_production', 'img_phone', 'img_bus', 'comments']
