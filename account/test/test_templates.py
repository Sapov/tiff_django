from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from account.models import Organisation, DeliveryAddress

User = get_user_model()


class ProfileTemplatesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_list_profile(self):
        ''' Проверка страницы list профиля пользователя'''
        response = self.authorized_client.get('/account/list_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile_list.html')


class AccountTemplatesDeliveryAddressTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_delivery_address(self):
        '''Шаблон добавление адреса доставки'''
        response = self.authorized_client.get('/account/delivery_create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/deliveryaddress_form.html')

    def test_delivery_address_list(self):
        ''' Проверка страницы list адреса доставки пользователя'''
        response = self.authorized_client.get('/account/delivery_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/delivery_list.html')

    # def test_delete_delivery_address_item(self):
    #     '''Шаблон удаления адреса доставки  '''
    #     usr = User.objects.get(username='testUser')
    #     DeliveryAddress.objects.create(region='Тамбовcкая область', city='г. Тамбов', street='Вязов')
    #     response = self.authorized_client.get('/account/delivery_delete/1')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, '/account/deliveryaddress_confirm_delete.html')


class AccountTemplatesOrganisationTests(TestCase):
    ''' CRUD шаблоны работа с моделью Organisation'''

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_organisation(self):
        ''' Проверка наличия шаблона добавить организацию пользователя'''
        response = self.authorized_client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/organisation_form.html')

    def test_list_organisation(self):
        ''' Проверка наличия шаблона list организаций пользователя'''
        response = self.authorized_client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/organisation_list.html')

    def test_delete_organisation_template(self):
        '''Шаблон подтверждения удаления организации НЕ ЧЕГО УДАЛЯТЬ НУЖНО СНАЧАЛА ДОБАВИТЬ'''

        Organisation.objects.create(name_ul="OOO Рога и Копыты")
        response = self.authorized_client.get('/account/delete_organisation_user/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/organisation_confirm_delete.html')

    def test_update_organisations_template(self):
        ''' тест шаблона изменения записи Организации'''
        Organisation.objects.create(name_ul='Рога и копыта')
        response = self.authorized_client.get('/account/update_organisation_user/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/organisation_update_form.html')


class ItemModelTest(TestCase):
    '''тест модели элемента'''

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_saving_and_retrieving_item(self):
        '''Тест сохранения и получения элемента списка'''
        Organisation.objects.create(name_ul="OOO Рога и Копыты")
        saved_organisation = Organisation.objects.all()
        self.assertEqual(saved_organisation.count(), 1)
