from django import forms
from .models import *


class UploadFiles(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['material', "quantity", 'width', 'length', 'images']


class UpdateFiles(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['material', "quantity", 'width', 'length', 'images']


class AddFiles(forms.Form):
    # material = forms.ModelChoiceField(queryset=Material.objects.filter(type_print=1))
    quantity = forms.CharField(max_length=29)

