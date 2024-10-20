from django.contrib.auth import get_user_model
from django.test import TestCase

from files.models import Material, TypePrint, FinishWork
from files.tiff_file import Calculator

User = get_user_model()


class TestCalculator(TestCase):
    # добавить таблицу материал и загрузить туда тестовый материал!!!

    @classmethod
    def setUpTestData(cls):
        Material.objects.create(name='Баннер 440 грамм',
                                type_print=TypePrint.objects.create(type_print='Широкоформатная печать',
                                                                    info_type_print='Описание печати'),
                                price_contractor=200,
                                price=350,
                                price_customer_retail=400,
                                resolution_print=72,
                                is_active=True)
        FinishWork.objects.create(work='Порезка по краям',
                                  price_contractor=40,
                                  price=75,
                                  price_customer_retail=80,
                                  is_active=True)
        User.objects.create(username='testUser', role='CUSTOMER_RETAIL')
        User.objects.create(username='testUserAgent', role='CUSTOMER_AGENCY', email='agents@mail.ru')

    def test_change_role_user(self):
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=1)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 2,
                      'width': 2,
                      'role': user.role}
        item_image = Calculator(dict_param)
        results = item_image._change_role_user()
        self.assertEqual(results, (400, 80,))

    def test_change_role_user_agents(self):
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=2)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 2,
                      'width': 2,
                      'role': user.role}
        item_image = Calculator(dict_param)
        results = item_image._change_role_user()
        self.assertEqual(results, (350, 75,))

    def test_calculate_price(self):
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=1)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 2,
                      'width': 2,
                      'role': user.role}

        item_image = Calculator(dict_param)
        results = item_image.calculate_price()
        self.assertEqual(results, ((2 * 2) * 400) + (2 + 2) * 2 * 80)

    def test_calculate_cost(self):
        '''Считаем себестоимость по contractor price'''
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=1)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 2,
                      'width': 2,
                      'role': user.role}

        item_image = Calculator(dict_param)
        results = item_image.calculate_cost()
        self.assertEqual(results, ((2 * 2) * 200) + (2 + 2) * 2 * 40)

    def test_result(self):
        '''При маленьких размерах стоимость равна 1000'''
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=1)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 0.2,
                      'width': 0.2,
                      'role': user.role}

        item_image = Calculator(dict_param)
        results = item_image.calculate_price()
        self.assertEqual(results, 1000)

    def test_calculate_price_agents(self):
        material = Material.objects.get(id=1)
        finishing = FinishWork.objects.get(id=1)
        user = User.objects.get(id=2)
        dict_param = {'quantity': 1,
                      'material': material,
                      'finishing': finishing,
                      'length': 2,
                      'width': 2,
                      'role': user.role}

        item_image = Calculator(dict_param)
        results = item_image.calculate_price()
        self.assertEqual(results, 2000)
