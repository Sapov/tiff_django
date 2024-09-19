from django import forms

from delivery_in_bus.models import OrdersDeliveryBus


class FormLoadImgCourier(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_production', 'img_phone', 'img_bus', 'comments']
