from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from ..models import Organisation

User = get_user_model()


class AccountURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.organisation = Organisation.objects.create(
            user=self.user,
            name_full='Test Company',
            address='Test Address',
            address_post='Test Post Address',
            phone='123456',
            email='test@example.com',
            inn='123456789012',
            kpp='123456789',
        )

    def test_add_organisation(self):
        ''' Проверка страницы Оранизации пользователя'''
        self.authorized_client.force_login(self.user)

        response = self.authorized_client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 200)


class TestAccount(TestCase):
    def test_add_organisation(self):
        ''' Редирект пользователя с /account/add_organisation/'''
        response = self.client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 302)

    def test_list_organisation(self):
        """ Редирект пользователя с /account/list_organisation/"""
        response = self.client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 302)



