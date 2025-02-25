from cProfile import label

from django import forms
from .models import *

class UserLids(forms.ModelForm):
    class Meta:
        model = Lids
        fields = ['username', 'email', 'phone', 'interest', 'interest_text']


# class UserLids(forms.Form):
#     username = forms.CharField(max_length=255, label = 'Имя')
#     email = forms.EmailField(max_length=255, label = 'Укажите почту', required=True)
#     phone = PhoneNumberField()
#     interest = forms.ModelChoiceField(
#         queryset=Interest.objects.all(),
#         label="Тема сообщения",
#         help_text="выбрать тему",
#         initial=1,
#     )
#     interest_text = forms.CharField(max_length=255, label = 'Имя')


