from files.models import FinishWork
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
        work = FinishWork.objects.get(id=1)
        # Получение метаданных поля для получения необходимых значений
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
        expected_object_name = f'{work.work} - {work.price} руб./1 м.п.'
        self.assertEquals(expected_object_name, str(work))

    def test_model_verbose_name(self):
        """Тест поля verbose_name модели FinishWork"""

        self.assertEqual(FinishWork._meta.verbose_name, 'Финишная обработка')

    def test_model_verbose_name_plural(self):
        """Тест поля verbose_name_plural модели TriFinishWorkal"""

        self.assertEqual(FinishWork._meta.verbose_name_plural, 'Финишные обработки')