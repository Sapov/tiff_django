from django.contrib.auth import get_user_model

from files.models import FinishWork, TypePrint, Material, UseCalculator, Contractor, StatusProduct, Product
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


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

    def test_fields_price_customer_retail_max_length(self):
        work = FinishWork.objects.get(id=1)
        expected_max_length = work._meta.get_field('price_customer_retail').max_length
        self.assertEqual(expected_max_length, 100)

    def test_help_text_customer_retail(self):
        work = FinishWork.objects.get(id=1)
        expected_help_text = work._meta.get_field('price_customer_retail').help_text
        self.assertEqual(expected_help_text, 'Цена за 1 м. погонный')

    def test_verbose_name_customer_retail(self):
        work = FinishWork.objects.get(id=1)
        expected_verbose_name = work._meta.get_field('price_customer_retail').verbose_name
        self.assertEqual(expected_verbose_name, 'Стоимость работы розница в руб.')

    def test_null_customer_retail(self):
        work = FinishWork.objects.get(id=1)
        expected_bool = work._meta.get_field('price_customer_retail').null
        self.assertEqual(expected_bool, True)
        # self.assertTrue(expected_bool)

    def test_fields_is_active(self):
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('is_active').verbose_name
        expected_verbose_name = 'Активный'
        self.assertEquals(field_label, expected_verbose_name)

    def test_filed_blank_customer_retail(self):
        work = FinishWork.objects.get(id=1)
        expected_bool = work._meta.get_field('price_customer_retail').blank
        self.assertTrue(expected_bool)

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


class TestModelContractor(TestCase):
    @classmethod
    def setUpTestData(cls):
        Contractor.objects.create(name='Рога и Копыта',
                                  description='Спекулянты',
                                  email_contractor='roga@copita.ru',
                                  phone_contractor='123',
                                  phone_contractor_2='234',
                                  address='г. Тамбов',
                                  contact_contractor='Петька')

    def test_name_label(self):
        item = Contractor.objects.get(id=1)
        field_label = item._meta.get_field('name').verbose_name
        expected_name = 'Наименование организации'
        self.assertEqual(field_label, expected_name)

    def test_name_max_length(self):
        item = Contractor.objects.get(id=1)
        field_label = item._meta.get_field('name').max_length
        expected_max_length = 100
        self.assertEqual(field_label, expected_max_length)


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
        self.assertEqual(field_label, expected_verbose_name)

    def test_max_length_type_print(self):
        type_print = TypePrint.objects.get(id=1)  # Получение объекта для тестирования
        max_length = type_print._meta.get_field(
            'type_print').max_length  # Получение метаданных поля для получения необходимых значений
        self.assertEqual(max_length, 128)  # Сравнить значение с ожидаемым результатом

    def test_fields_info_type_print(self):
        type_print = TypePrint.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = type_print._meta.get_field('info_type_print').verbose_name
        expected_verbose_name = 'Описание метода печати'
        self.assertEqual(field_label, expected_verbose_name)

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

    def test_fields_type_print(self):
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

    # --------TEST-----price_customer_retail----------
    def test_fields_price_customer_retail(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price_customer_retail').verbose_name
        expected_verbose_name = 'Стоимость печати розница в руб.'
        self.assertEquals(field_label, expected_verbose_name)

    def test_price_customer_retail_help_text(self):
        work = Material.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
        field_label = work._meta.get_field('price_customer_retail').help_text
        expected_verbose_name = 'За 1 м2'
        self.assertEquals(field_label, expected_verbose_name)

    def test_max_length_price_customer_retail(self):
        work = Material.objects.get(id=1)  # Получение объекта для тестирования
        max_length = work._meta.get_field(
            'price_customer_retail').max_length  # Получение метаданных поля для получения необходимых значений
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

    def test_string_representation(self):
        """Тест строкового отображения"""
        work = Material.objects.get(id=1)  # Получение объекта для тестирования
        expected_object_name = f'{work.name} {work.type_print}'
        self.assertEquals(expected_object_name, str(work))

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели FinishWork"""

        self.assertEqual(Material._meta.verbose_name, 'Материал')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели TriFinishWorkal"""

        self.assertEqual(Material._meta.verbose_name_plural, 'Материалы для печати')


class TestStatusProduct(TestCase):
    @classmethod
    def setUpTestData(cls):
        StatusProduct.objects.create(status='Оформлен')

    def test_field_status_verbose_name(self):
        status = StatusProduct.objects.get(id=1)
        field_label = status._meta.get_field('status').verbose_name
        expected_verbose_name = 'Статус файла'
        self.assertEqual(field_label, expected_verbose_name)

    def test_field_status_max_length(self):
        status = StatusProduct.objects.get(id=1)
        field_label = status._meta.get_field('status').max_length
        expected_verbose_name = 64
        self.assertEqual(field_label, expected_verbose_name)



class TestModelsUseCalculator(TestCase):
    """Тесты для модели UseCalculator"""

    @classmethod
    def setUpTestData(cls):
        """Заносит данные в БД перед запуском тестов класса"""
        Material.objects.create(name='Баннер 440 грамм ламинированный',  # type_print='Интерьерная печать',
                                price_contractor=200, price=400, resolution_print=100)
        fw = FinishWork.objects.create(work='Порезка', price_contractor=50, price=100, price_customer_retail=200,
                                       is_active=True)

        UseCalculator.objects.create(material=Material.objects.get(id=1),
                                     quantity=2, width=2, length=3, results=3800,
                                     FinishWork=FinishWork.objects.get(id=1), )

        # created_at = 2004/01/01

    def test_material_label(self):
        '''Получение метаданных поля для получения необходимых значений'''
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('material').verbose_name
        expected_verbose_name = 'Материал'
        self.assertEquals(field_label, expected_verbose_name)

    def test_quantity_label(self):
        '''Получение метаданных поля для получения необходимых значений'''
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('quantity').verbose_name
        expected_verbose_name = 'Количество'
        self.assertEquals(field_label, expected_verbose_name)

    def test_quantity_help_text(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('quantity').help_text
        expected_help_text = 'Введите количество'
        self.assertEqual(field_label, expected_help_text)

    def test_quantity_default(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('quantity').default
        expected_default = 1
        self.assertEqual(field_label, expected_default)

    def test_width_label(self):
        '''Получение метаданных поля для получения необходимых значений'''
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('width').verbose_name
        expected_verbose_name = 'Ширина'
        self.assertEquals(field_label, expected_verbose_name)

    def test_width_help_text(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('width').help_text
        expected_help_text = 'Указывается в см.'
        self.assertEqual(field_label, expected_help_text)

    def test_width_default(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('width').default
        expected_default = 0
        self.assertEqual(field_label, expected_default)

    def test_length_label(self):
        '''Получение метаданных поля для получения необходимых значений'''
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('length').verbose_name
        expected_verbose_name = 'Длина'
        self.assertEquals(field_label, expected_verbose_name)

    def test_length_help_text(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('length').help_text
        expected_help_text = 'Указывается в см.'
        self.assertEqual(field_label, expected_help_text)

    def test_length_default(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('length').default
        expected_default = 0
        self.assertEqual(field_label, expected_default)

    def test_results_label(self):
        '''Получение метаданных поля для получения необходимых значений'''
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('results').verbose_name
        expected_verbose_name = 'Стоимость'
        self.assertEquals(field_label, expected_verbose_name)

    def test_results_max_digits(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('results').max_digits
        expected_max_digit = 10
        self.assertEqual(field_label, expected_max_digit)

    def test_results_decimal_places(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('results').decimal_places
        expected_decimal_places = 2
        self.assertEqual(field_label, expected_decimal_places)

    def test_results_default(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('results').default
        expected_decimal_places = 0
        self.assertEqual(field_label, expected_decimal_places)

    def test_results_blank(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('results').blank
        expected_blank = True
        self.assertEqual(field_label, expected_blank)

    def test_Finishwork_verbose_name(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('FinishWork').verbose_name
        expected_verbose_name = 'Финишная обработка'
        self.assertEqual(field_label, expected_verbose_name)

    def test_Finishwork_default(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('FinishWork').default
        expected_decimal_places = 1
        self.assertEqual(field_label, expected_decimal_places)

    def test_fild_created_at(self):
        item = UseCalculator.objects.get(id=1)
        field_label = item._meta.get_field('created_at').verbose_name
        expected_verbose_name = 'Добавлено'
        self.assertEqual(field_label, expected_verbose_name)

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели UseCalculator"""
        self.assertEqual(UseCalculator._meta.verbose_name, 'Расчет клиентов сайта')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели UseCalculator"""
        self.assertEqual(UseCalculator._meta.verbose_name_plural, 'Расчеты клиентов сайта')

    def test_string_representation(self):
        """Тест строкового отображения"""
        work = UseCalculator.objects.get(id=1)  # Получение объекта для тестирования
        # expected_object_name = '%s, %s, %s' % (work.work, work.price_contractor, work.price)
        expected_object_name = (f'Дата: {str(work.created_at)[:16]} /{str(work.material)[:10]}/ '
                                f'Кол-во: {work.quantity}шт./Размер: {work.width}x{work.length}м./Стоимость: '
                                f'{work.results} руб.')

        self.assertEquals(expected_object_name, str(work))
