import logging

from django import forms

from users.models import User
from .models import Order

# class AddNewOrder(forms.Form):
#     organisation_payer = forms.ModelChoiceField(queryset=Order.objects.filter(user=request.user))

from django import forms
from django.contrib.auth import get_user_model
from account.models import Organisation, DeliveryAddress


class NewOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            # "organisation_payer",
            "delivery_address",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(NewOrder, self).__init__(*args, **kwargs)
        self.fields["delivery_address"].queryset = DeliveryAddress.objects.filter(
            user=self.user
        )
