from django.test import TestCase
from django.urls import reverse, resolve

from files.views import index


class HomePageTests(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_home_page_template(self):
        response = self.client.get(reverse(index))
        self.assertTemplateUsed(response, 'index.html')

    def test_home_page_url(self):
        ''' перенаправление на страницу с авторизацией'''
        response = self.client.get('/')
        self.assertRedirects(response, '/users/login/?next=/')

    def test_home_page_function(self):
        """ проверка что мы ссылаемся на функцию index"""
        found = resolve('/')
        self.assertEqual(found.func, index)
