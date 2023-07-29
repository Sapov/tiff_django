from django.test import TestCase


class TestFiles(TestCase):
    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)

    def test_all_files(self):
        response = self.client.get('/allfiles/')
        self.assertEqual(response.status_code, 302)

    def test_price(self):
        response = self.client.get('/price/')
        self.assertEqual(response.status_code, 302)
