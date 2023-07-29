from django.test import TestCase

from django.test import TestCase


class TestAccount(TestCase):
    def test_add_organisation(self):
        response = self.client.get('/account/add_organisation/')
        self.assertEqual(response.status_code, 302)

    def test_list_organisation(self):
        response = self.client.get('/account/list_organisation/')
        self.assertEqual(response.status_code, 302)
