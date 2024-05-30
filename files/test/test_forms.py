from django.test import TestCase

# Создайте ваши тесты здесь

import datetime
from django.utils import timezone
from files.forms import CalculatorLargePrint


class CalculatorLargePrintFormTest(TestCase):
    '''тест для формы CalculatorLargePrint'''
    def test_CalculatorLargePrint_form_field_label_quantity(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['quantity'].label == None or form.fields['quantity'].label == 'Количество')

    def test_CalculatorLargePrint_form_field_value_max_quantity(self):
        form = CalculatorLargePrint()
        self.assertTrue(form.fields['quantity'].max_value == 1000)

    def test_CalculatorLargePrint_form_field_initial(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['quantity'].initial == 1)

    def test_CalculatorLargePrint_form_field_label_material(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['material'].label == None or form.fields['material'].label == 'Материал для печати')

    def test_CalculatorLargePrint_form_field_helptext_material(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['material'].help_text == None or form.fields['material'].help_text == 'Выберите материал')

    def test_CalculatorLargePrint_form_field_label_finishka(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['finishka'].label == None or form.fields['finishka'].label == 'Обработка')

    def test_CalculatorLargePrint_form_field_label_length(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['length'].label == None or form.fields['length'].label == 'Длина в метрах')

    def test_CalculatorLargePrint_form_field_label_width(self):
        form = CalculatorLargePrint()
        self.assertTrue(
            form.fields['width'].label == None or form.fields['width'].label == 'Ширина в метрах')
