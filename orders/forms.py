import logging
from django import forms
from account.models import Organisation, DeliveryAddress

from users.models import User
from .models import Order

# class AddNewOrder(forms.Form):
#     organisation_payer = forms.ModelChoiceField(queryset=Order.objects.filter(user=request.user))

from django.contrib.auth import get_user_model
from account.models import Organisation


# class NewOrder(forms.ModelForm):
#     class Meta:
#         model = Order
#         # fields = ['organisation_payer', 'delivery']
#         fields = ['delivery']
#
#     # def __init__(self, *args, **kwargs):
#     #     self.user = kwargs.pop('user', None)
#     #     super(NewOrder, self).__init__(*args, **kwargs)
#     #     self.fields['organisation_payer'].queryset = Organisation.objects.filter(
#     #         Contractor=self.user)  # для агенства раскоментировать


class ReportForm(forms.Form):
    date_start = forms.DateTimeInput()
    date_finish = forms.DateTimeInput()


# class AddNewOrder(forms.Form):
#     organisation_payer = forms.ModelChoiceField(queryset=Order.objects.filter(user=request.user))


class NewOrder(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "organisation_payer",
            # "delivery_address",
            'delivery',
            # "date_complete",
        ]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(NewOrder, self).__init__(*args, **kwargs)
        # self.fields["delivery_address"].queryset = DeliveryAddress.objects.filter(
        #     user=self.user
        # )
