from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.forms import UserCreationForm

User = get_user_model()


class TestRegistration(TestCase):
    def test_get(self):
        """Проверка получения формы"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserCreationForm)

    def test_post_error(self):
        """Тест регистрации с ошибкой"""
        email = 'test@mail.ru'
        payload = {
            'username': 'testuser',
            'email': email,
            'password1': '1111',
        }
        response = self.client.post(reverse('register'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn('password2', response.context['form'].errors)

    def test_post_form(self):
        email = 'test@mail.ru'
        payload = {
            'username': 'testuser',
            'email': email,
            'password1': 'Kdhedhfc78',
            'password2': 'Kdhedhfc78',
        }
        response = self.client.post(reverse('register'), payload)
        user = User.objects.get(email=email)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, email)
        self.assertTrue(user.is_authenticated)
