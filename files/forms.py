from django import forms
from django.core.validators import FileExtensionValidator

from .models import *
from .validators import validate_tiff_file


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


class CalculatorForm(forms.Form):
    quantity = forms.FloatField(max_value=1000, label="Количество", initial=1)
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        label="Материал для печати",
        help_text="Выберите материал",
        initial=1,
    )
    finishing = forms.ModelChoiceField(
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
    finishing = forms.ModelChoiceField(
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
    finishing = forms.ModelChoiceField(
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
    finishing = forms.ModelChoiceField(
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
    finishing = forms.ModelChoiceField(
        queryset=FinishWork.objects.all(), label="Обработка", initial=True)
    length = forms.FloatField(max_value=100, label="Длина в метрах")
    width = forms.FloatField(max_value=100, label="Ширина в метрах")


class BaseUploadForm(forms.ModelForm):
    """Базовая форма для всех типов печати"""

    # Общие поля для всех форм
    TYPE_PRINT = None  # Переопределяется в дочерних классах
    DEFAULT_MATERIAL = None  # Переопределяется в дочерних классах
    FINISH_WORK = None # Переопределяется в дочерних классах

    material = forms.ModelChoiceField(
        queryset=Material.objects.none(),  # Будет переопределено
        label="Выберите материал для печати"
    )
    # FinishWork = forms.ModelChoiceField(
    #     queryset=FinishWork.objects.all(),
    #     label="Финишная обработка",
    #     initial=FINISH_WORK,
    # )

    class Meta:
        model = Product
        fields = [
            "quantity",
            "material",
            "FinishWork",
            "images",
            "comments"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Устанавливаем queryset для material на основе TYPE_PRINT
        self.fields['material'].queryset = Material.objects.filter(type_print=self.TYPE_PRINT)
        self.fields['material'].initial = self.DEFAULT_MATERIAL
        self.fields['FinishWork'].initial = self.FINISH_WORK
        """Форма загрузки файлов (только TIFF)"""
        self.fields['images'].validators.append(validate_tiff_file)
        self.fields['images'].widget.attrs.update({'accept': '.tif,.tiff'})


class UploadFilesInter(BaseUploadForm):
    """Форма загрузки файлов для интерьерной печати"""

    TYPE_PRINT = 2
    DEFAULT_MATERIAL = 22  # пленка матовая Китай
    FINISH_WORK = 2


class UploadFilesLarge(BaseUploadForm):
    """Форма загрузки файлов для широкоформатной печати """

    TYPE_PRINT = 1
    DEFAULT_MATERIAL = 1  # 440 баннер
    FINISH_WORK = 1 # поля по 5 см



class UploadFilesUV(BaseUploadForm):
    """Форма загрузки файлов для UV-печати"""

    TYPE_PRINT = 3
    DEFAULT_MATERIAL = 37  # ПВХ 3 мм
    FINISH_WORK = 2


class UploadFilesRollUp(forms.ModelForm):
    """Форма загрузки файлов для интерьерной печати полотна для Роллапа"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(id=21),
        # id=21  это литой баннер Интрьерная печать для Ролапа
        label="Выберите материал для печати",
        initial=22,  # по умолчанию литой 450 грамм

    )
    FinishWork = forms.ModelChoiceField(
        queryset=FinishWork.objects.filter(id=2),
        label="Финишная обработка",
        initial=2,
    )

    class Meta:
        model = Product
        fields = ["quantity", 'images']


class UploadFilesPictures(forms.ModelForm):
    """Форма загрузки файлов для интерьерной печати полотна для Роллапа"""

    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(type_print=5),
        label="Выберите материал для печати",

    )
    FinishWork = forms.ModelChoiceField(
        queryset=FinishWork.objects.filter(id=2),
        label="Финишная обработка",
        initial=2,
    )

    class Meta:
        model = Product
        fields = ["quantity", 'images']


class CreateContractor(forms.ModelForm):
    class Meta:
        model = Contractor
        fields = ["name", "description", "email_contractor", "phone_contractor", "phone_contractor_2",
                  'address', 'contact_contractor']
