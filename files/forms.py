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


###
class Calculator(forms.Form):
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1,
    )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True
    )
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")


class CalculatorLargePrint(forms.Form):
    '''для широкоформатной печати'''
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=1),
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1, )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True)
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")


class CalculatorInterierPrint(forms.Form):
    '''для интерьерной печати'''
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=2),
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1, )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True)
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")


class CalculatorUVPrint(forms.Form):
    '''для интерьерной печати'''
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=3),  # УФ
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1, )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True)
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")


class CalculatorBlankMaterial(forms.Form):
    '''для расчета чистого материала'''
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=4),  # пустой материал
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1, )
    finishka = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True)
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
            "material",
            "FinishWork",
            "images",
            "comments"
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
            "material",
            "FinishWork",
            "images",
            "comments"
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
            "material",
            "FinishWork",
            "images",
            "comments"
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
        label="Финишная обработка",
        initial=2,
    )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "images",
            # "FinishWork",
            "material",
        ]


class CreateContractor(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ["name", "description", "email_contractor", "phone_contractor", "phone_contractor_2",
                  'address', 'contact_contractor']
