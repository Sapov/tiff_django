from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class ProfileTemplatesTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_list_profile(self):
        ''' Проверка страницы list профиля пользователя'''
        response = self.authorized_client.get('/profile_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_list.html')

    def test_profile_edit_template(self):
        response = self.authorized_client.get('/profile_edit/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/edit_profile.html')
