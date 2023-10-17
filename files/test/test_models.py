from files.models import FinishWork, TypePrint, Material
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
            price=200,
            is_active=True)

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


    def test_fields_is_active(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('is_active').verbose_name
        expected_verbose_name = 'Активный'
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


class TestModelsMaterial(TestCase):
    """Тесты для модели Material"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        Material.objects.create(
            name='Баннер 440 грамм ламинированный',
            # type_print='Интерьерная печать',
            price_contractor=100,
            price=200,
            resolution_print=100)

    def test_field_name(self):
        '''Получение метаданных поля для получения необходимых значений'''
        name = Material.objects.get(id=1)
        field_label = name._meta.get_field('name').verbose_name
        expected_verbose_name = 'Материал для печати'
        self.assertEquals(field_label, expected_verbose_name)

    #
    def test_max_length_name_field(self):
        name = Material.objects.get(id=1)  # Получение объекта для тестирования
        max_length = name._meta.get_field(
            'name').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_fields_ptype_print(self):
        type_print = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = type_print._meta.get_field('type_print').verbose_name
        expected_verbose_name = 'Тип печати'
        self.assertEquals(field_label, expected_verbose_name)

    def test_fields_price_contractor_help_text(self):
        price_contractor = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = price_contractor._meta.get_field('price_contractor').help_text
        expected_verbose_name = 'За 1 м2'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_price_contractor(self):
        work = Material.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_fields_price_contractor_verbose_name(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price_contractor').verbose_name
        expected_verbose_name = 'Себестоимость печати в руб.'
        self.assertEquals(field_label, expected_verbose_name)

    def test_fields_price_verbose_name(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price').verbose_name
        expected_verbose_name = 'Стоимость печати для РА в руб.'
        self.assertEquals(field_label, expected_verbose_name)

    #
    def test_fields_price_help_text(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price').help_text
        expected_verbose_name = 'За 1 м2'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_price(self):
        work = Material.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'price_contractor').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_fields_resolution_print_verbose_name(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('resolution_print').verbose_name
        expected_verbose_name = 'DPI'
        self.assertEquals(field_label, expected_verbose_name)

    def test_fields_resolution_print_help_text(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('resolution_print').help_text
        expected_verbose_name = 'разрешение для печати на материале'
        self.assertEquals(field_label, expected_verbose_name)

    # def test_max_length_presolution_print(self):
    #     work = Material.objects.get(id=1)  # Получение объекта для тестирования
    #     max_length = work._meta.get_field(
    #         'resolution_print').max_length  # Получение метаданных поля для получения необходимых значений
    #     self.assertEquals(max_length, 100)  # Сравнить значение с ожидаемым результатом

    def test_string_representation(self):
        """Тест строкового отображения"""
        work = Material.objects.get(id=1)  # Получение объекта для тестирования
        expected_object_name = f'{work.name} - {work.type_print}'
        self.assertEquals(expected_object_name, str(work))

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели FinishWork"""

        self.assertEqual(Material._meta.verbose_name, 'Материал')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели TriFinishWorkal"""

        self.assertEqual(Material._meta.verbose_name_plural, 'Материалы для печати')
