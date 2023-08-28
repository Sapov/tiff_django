from files.models import FinishWork, TypePrint
from django.test import TestCase
from django.urls import reverse


class TestModelsFinishWork(TestCase):
    """Тесты для модели FinishWork"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        FinishWork.objects.create(
            work='Порезка баннера',
            price_contractor=100,
            price=200)

    def test_work(self):
        '''Получение метаданных поля для получения необходимых значений'''
        work = FinishWork.objects.get(id=1)
        field_label = work._meta.get_field('work').verbose_name
        expected_verbose_name = 'Финишная обработка'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_work(self):
        work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'work').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 255)  # Сравнить значение с ожидаемым результатом

    def test_fields_price_contractor(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price_contractor').verbose_name
        expected_verbose_name = 'Себестоимость работы в руб.'
        self.assertEquals(field_label, expected_verbose_name)

    def test_fields_price_contractor_help_text(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price_contractor').help_text
        expected_verbose_name = 'Цена за 1 м. погонный'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_price_contractor(self):
        work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_fields_price_verbose_name(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price').verbose_name
        expected_verbose_name = 'Стоимость работы в руб.'
        self.assertEquals(field_label, expected_verbose_name)

    def test_fields_price_help_text(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price').help_text
        expected_verbose_name = 'Цена за 1 м. погонный'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_price(self):
        work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_string_representation(self):
        """Тест строкового отображения"""
        work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
        # expected_object_name = '%s, %s, %s' % (work.work, work.price_contractor, work.price)
        expected_object_name = f'{work.work}'
        self.assertEquals(expected_object_name, str(work))

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели FinishWork"""

        self.assertEqual(FinishWork._meta.verbose_name, 'Финишная обработка')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели TriFinishWorkal"""

        self.assertEqual(FinishWork._meta.verbose_name_plural, 'Финишные обработки')


class TestModelsTypePrint(TestCase):
    """Тесты для модели TypePrint"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        TypePrint.objects.create(
            type_print='Интерьерная печать',
            info_type_print=' Интретьерная печать харктеризуется мелкой детализацией и предназначена'
                            'для размещения внутри помещения')

    def test_type_print(self):
        '''Получение метаданных поля для получения необходимых значений'''
        type_print = TypePrint.objects.get(id=1)
        field_label = type_print._meta.get_field('type_print').verbose_name
        expected_verbose_name = 'Метод печати'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_type_print(self):
        type_print = TypePrint.objects.get(id=1)  # Получение объекта для тестирования
        max_length = type_print._meta.get_field(
            'type_print').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 128)  # Сравнить значение с ожидаемым результатом

    def test_fields_info_type_print(self):
        type_print = TypePrint.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = type_print._meta.get_field('info_type_print').verbose_name
        expected_verbose_name = 'Описание метода печати'
        self.assertEquals(field_label, expected_verbose_name)

    # def test_fields_price_contractor_help_text(self):
    #     work = FinishWork.objects.get(id=1)
    #     # Получение метаданных поля для получения необходимых значений
    #     field_label = work._meta.get_field('price_contractor').help_text
    #     expected_verbose_name = 'Цена за 1 м. погонный'
    #     self.assertEquals(field_label, expected_verbose_name)

    # def test_max_length_price_contractor(self):
    #     work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
    #     max_length = work._meta.get_field(
    #         'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
    #     self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    # def test_fields_price_verbose_name(self):
    #     work = FinishWork.objects.get(id=1)
    #     # Получение метаданных поля для получения необходимых значений
    #     field_label = work._meta.get_field('price').verbose_name
    #     expected_verbose_name = 'Стоимость работы в руб.'
    #     self.assertEquals(field_label, expected_verbose_name)

    # def test_fields_price_help_text(self):
    #     work = FinishWork.objects.get(id=1)
    #     # Получение метаданных поля для получения необходимых значений
    #     field_label = work._meta.get_field('price').help_text
    #     expected_verbose_name = 'Цена за 1 м. погонный'
    #     self.assertEquals(field_label, expected_verbose_name)

    # def test_max_length_price(self):
    #     work = FinishWork.objects.get(id=1)  # Получение объекта для тестирования
    #     max_length = work._meta.get_field(
    #         'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
    #     self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_string_representation_TypePrint(self):
        """Тест строкового отображения __str__"""
        type_print = TypePrint.objects.get(id=1)  # Получение объекта для тестирования
        # expected_object_name = '%s, %s, %s' % (work.work, work.price_contractor, work.price)
        expected_object_name = f'{type_print.type_print}'
        self.assertEquals(expected_object_name, str(type_print))

    def test_model_verbose_name_TypePrint(self):
        """Тест поля verbose_name модели FinishWork"""

        self.assertEqual(TypePrint._meta.verbose_name, 'Тип печати')

    def test_model_verbose_name_plural_TypePrint(self):
        """Тест поля verbose_name_plural модели TriFinishWorkal"""

        self.assertEqual(TypePrint._meta.verbose_name_plural, 'Типы печати')