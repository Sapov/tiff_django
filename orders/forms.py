from django import forms

from .models import Order

# class AddNewOrder(forms.Form):
#     organisation_payer = forms.ModelChoiceField(queryset=Order.objects.filter(user=request.user))

from django import forms
from django.contrib.auth import get_user_model
from account.models import Organisation


class UserOrganisationForm(forms.Form):

    def __init__(self, *args, **kwargs):

        super(UserOrganisationForm, self).__init__(*args, **kwargs)
        self.fields['organization'] = forms.ModelChoiceField(queryset=Organisation.objects.filter(Contractor=user))

    class Meta:
        model = Order
        fields = ['organisation_payer']


User = get_user_model()
