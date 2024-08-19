from django.contrib.auth import get_user_model
from django.test import Client, TestCase

User = get_user_model()


class AccountTemplatesTests(TestCase):

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_list_profile(self):
        ''' Проверка страницы list профиля пользователя'''
        response = self.authorized_client.get('/account/list_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_list.html')

    def test_create_organisation(self):
        ''' Проверка наличия шаблона добавить организацию пользователя'''
        response = self.authorized_client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/organisation_form.html')

    def test_list_organisation(self):
        ''' Проверка наличия шаблона list организаций пользователя'''
        response = self.authorized_client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'organisation_list.html')