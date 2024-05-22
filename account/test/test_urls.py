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


class TestModelProfile(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all
        # test methods
        Profile.objects.create(
            user=User.objects.create(username='vasa'),
            date_of_birth="2023-04-07",

            phone='47786786',
            telegram='4545645645',
            organisation=Organisation.objects.create(id=1),

        )

    def test_date_of_birth_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('date_of_birth').verbose_name
        self.assertEqual(field_label, 'Дата рождения')

    def test_telegram_length(self):
        profile = Profile.objects.get(id=1)
        max_length = profile._meta.get_field('telegram').max_length
        self.assertEqual(max_length, 15)
