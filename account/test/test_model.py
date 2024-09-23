from django.contrib.auth import get_user_model
from unittest import TestCase
from account.models import Organisation, Delivery

User = get_user_model()


#

class TestModelDelivery(TestCase):
    def setUp(self):
        Delivery.objects.create(type_delivery='На ослах')

    def test_type_delivery_verbose_name(self):
        delivery = Delivery.objects.get(id=1)
        field_label = delivery._meta.get_field('type_delivery').verbose_name
        expected_delivery_verbose_name = 'Тип доставки'
        self.assertEqual(field_label, expected_delivery_verbose_name)

    def test_type_delivery_max_length(self):
        delivery = Delivery.objects.get(id=1)
        max_length = delivery._meta.get_field('type_delivery').max_length
        expected_max_length = 200
        self.assertEqual(max_length, expected_max_length)

    def test_type_delivery_default(self):
        delivery = Delivery.objects.get(id=1)
        default = delivery._meta.get_field('type_delivery').default
        expected_default = 2
        self.assertEqual(default, expected_default)

    def test_model_verbose_name(self):
        self.assertEqual(Delivery._meta.verbose_name, 'Тип Доставки')

    def test_model_verbose_name_plural(self):
        self.assertEqual(Delivery._meta.verbose_name_plural, 'Типы доставки')

    def test_model_ordering(self):
        self.assertEqual(Delivery._meta.ordering, ['type_delivery'])


class TestModelOrganisation(TestCase):

    def setUp(self):
        Organisation.objects.create(Contractor=User.objects.create(username='vasa'),
                                    name_full='ООО Ромашка',
                                    inn=123456789012,
                                    kpp=1234567,
                                    address='Полный адрес',
                                    bank_account='1231231231232',
                                    bank_name='sdfsdf',
                                    bik_bank='24234234',
                                    bankCorrAccount='13123123123',
                                    address_post='werwerw',
                                    phone='2342342342',
                                    email='sa@ds.ru'
                                    )

    # def test_Contractor_verbose_name(self):
    #     org = Organisation.objects.get(id=1)
    #     field_label = org._meta.get_field('Contractor').verbose_name
    #     expected_verbose_name = 'ЗАКАЗЧИК!!'
    #     self.assertEqual(field_label, expected_verbose_name)

    def test_inn_verbose_name(self):
        org = Organisation.objects.get(id=1)  # Получение объекта для тестирования
        max_length = org._meta.get_field(
            'inn').verbose_name  # Получение метаданных поля для получения необходимых значений
        self.assertEqual(max_length, 'ИНН')  # Сравнить значение с ожидаемым результатом

    # def test_max_length_inn(self):
    #     org = Organisation.objects.get(id=1)  # Получение объекта для тестирования
    #     max_length = org._meta.get_field('inn').max_length
    #     self.assertEqual(max_length, 100)
