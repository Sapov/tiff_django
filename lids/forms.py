from cProfile import label

from django import forms
from .models import Lids

class UserLids(forms.ModelForm):
    class Meta:
        model = Lids
        fields = ['username', 'email', 'phone', 'interest', 'interest_text']


    def __init__(self, *args, **kwargs):
        super(UserLids, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['phone'].required = True