from django import forms
from .models import *


class UploadFiles(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["material", "quantity", "width", "length", "images"]


class UpdateFiles(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["material", "quantity", "width", "length", "images"]


class AddFiles(forms.Form):
    # material = forms.ModelChoiceField(queryset=Material.objects.filter(type_print=1))
    quantity = forms.CharField(max_length=29)


class UploadArhive(forms.ModelForm):
    class Meta:
        model = UploadArh
        fields = "__all__"


class Calculator(forms.Form):
    quantity = forms.FloatField(max_value=1000, label="Количество")
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label="Материал для печати",
        help_text="Выберите материал",
        initial=True,
    )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True
    )
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")
