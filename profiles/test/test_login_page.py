from django.test import TestCase
from django.urls import resolve
from files.views import index


class TestLoginPage(TestCase):

    def test__login_page_correct(self):
        response = self.client.get('/')
        print(response)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

