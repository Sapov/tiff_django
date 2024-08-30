from django.test import Client, TestCase

from django.contrib.auth import get_user_model

Users = get_user_model()


class TestTemplatesOrders(TestCase):
    def setUp(self):
        self.user = Users.objects.create(username='TestUser')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_template_new_order(self):
        '''тест наличия шаблона new_order.html'''
        response = self.authorized_client.get('/orders/neworder/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'neworder.html')
