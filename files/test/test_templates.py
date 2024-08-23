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
    # def test_template_edit_file(self):
    #     '''Тест шаблона редактирования файла'''
    #     Product.objects.create(quantity=3)
    #     response = self.authorized_client.get('/files/edit/1')
    #     self.assertEqual(response.status_code, 200)