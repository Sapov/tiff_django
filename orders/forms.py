import logging

from django import forms

from users.models import User
from .models import Order

# class AddNewOrder(forms.Form):
#     organisation_payer = forms.ModelChoiceField(queryset=Order.objects.filter(user=request.user))

from django import forms
from django.contrib.auth import get_user_model
from account.models import Organisation




class NewOrder(forms.ModelForm):
    # organisation = forms.ModelChoiceField(queryset=Organisation.objects.none())

    class Meta:
        model = Order
        fields = ['organisation_payer']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(NewOrder, self).__init__(*args, **kwargs)
        self.fields['organisation_payer'].queryset=Organisation.objects.filter(Contractor=self.user)

        # logging.info(f'USER FORM{self.user}')
        # self.user_itm = User.objects.get(email=self.user)
        #
        # print(f'user_id{self.user_itm}')

