from django.test import Client, TestCase

from django.contrib.auth import get_user_model

from files.models import Product

User = get_user_model()


class FileTemplateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='userTest')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_template_list_files(self):
        response = self.authorized_client.get('/files/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_template_create_file(self):
        ''' Шаблон добавления файла'''
        response = self.authorized_client.get('/files/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/product_form.html')

    def test_template_price(self):
        response = self.authorized_client.get('/files/price/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'price.html')

    def test_template_calculator(self):
        '''Тест шаблона калькулятора'''
        response = self.authorized_client.get('/files/calculator/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculator.html')

    def test_templates_calculator_large_print_out(self):
        response = self.authorized_client.get('/files/calculator_large_print_out/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/calculator_large.html')

    def test_templates_calculator_interior_print_out(self):
        response = self.authorized_client.get('/files/calculator_interior_print/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/calculator_interior_print.html')

    def test_templates_calculator_blank_material(self):
        response = self.authorized_client.get('/files/calculator_blank/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'files/calculator_large.html')
