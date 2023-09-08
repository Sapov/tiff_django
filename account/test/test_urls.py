from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from http import HTTPStatus

from ..models import Organisation, Profile

User = get_user_model()


class AccountURLTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.organisation = Organisation.objects.create(
            Contractor=self.user,
            name_ul='Test Company',
            address_ur='Test Address',
            address_post='Test Post Address',
            phone='123456',
            email='test@example.com',
            inn='123456789012',
            kpp='123456789',
            okpo='123456789012',
        )


class TestAccount(TestCase):
    def test_add_organisation(self):
        ''' Редирект пользователя с /account/add_organisation/'''
        response = self.client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 302)

    def test_list_organisation(self):
        """ Редирект пользователя с /account/list_organisation/"""
        response = self.client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 302)

    def test_edit_profile(self):
        ''' Редирект пользователя с /account/edit/'''
        response = self.client.get('/account/edit/')
        self.assertEqual(response.status_code, 302)



