from django import forms

from delivery_in_bus.models import OrdersDeliveryBus


class FormLoadImg(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_production']


class FormLoadImgStepTwo(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_phone']


class FormLoadImgStepThree(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_bus']


class FormLoadImgStepFour(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['comments']


class FormLoadImgCourier(forms.ModelForm):
    class Meta:
        model = OrdersDeliveryBus
        fields = ['img_production', 'img_phone', 'img_bus', 'comments']
