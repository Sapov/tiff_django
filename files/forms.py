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


class UploadFilesInter(forms.ModelForm):
    """Форма загрузки файлов для интерьерной печати отфильтруем только интерьерную печать"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=2),
        label="Выберите материал для печати",
        initial=13,  # по умолчанию пленка матовая Китай
    )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "images",
            "FinishWork",
            "Fields",
            "material",
        ]


class UploadFilesLarge(forms.ModelForm):
    """Форма загрузки файлов для Широкоформатной печати отфильтруем только широкоформатную печать"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=1),
        label="Выберите материал для печати",
        initial=1,  # по умолчанию 440 баннер
    )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "images",
            "FinishWork",
            "Fields",
            "material",
        ]


class UploadFilesUV(forms.ModelForm):
    """Форма загрузки файлов для UV-печати отфильтруем только UV-печать"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=3),
        label="Выберите материал для печати",
        initial=1,  # по умолчанию ПВХ 3 мм
    )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "images",
            "FinishWork",
            "Fields",
            "material",
        ]


class UploadFilesRollUp(forms.ModelForm):
    """Форма загрузки файлов для интерьерной печати полотна для Роллапа"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=2),
        label="Выберите материал для печати",
        initial=20,  # по умолчанию литой 450 грамм
    )
    FinishWork = forms.ModelChoiceField(
        queryset=FinishWork.objects.filter(id=2),
        label="Финишная работа",
        initial=2,  # по умолчанию литой 450 грамм
    )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "images",
            "FinishWork",
            "Fields",
            "material",
        ]
