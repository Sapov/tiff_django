from django.test import TestCase
from django.urls import reverse

from orders.models import StatusOrder


class TestOrder(TestCase):
    def test_order_new(self):
        response = self.client.get('/orders/new_order/')
        self.assertEqual(response.status_code, 302)

    def test_view_orders(self):
        response = self.client.get('/orders/view_orders/')
        self.assertEqual(response.status_code, 302)

    def test_view_all_orders(self):
        response = self.client.get('/orders/view_all_orders/')
        self.assertEqual(response.status_code, 302)

    def test_view_all_files_for_work_in_orders(self):
        response = self.client.get('/orders/view_all_files_for_work_in_orders/')
        self.assertEqual(response.status_code, 302)

    # def test_tabl_bd_StatusOrder_create(self):
    #     StatusOrder.objects.create(name='Готовченко')
    #
    # def test_tabl_bd_StatusOrder_read(self):
    #     post = StatusOrder.objects.get(id=1)
    #     expected_object = f'{post.name}'
    #     self.assertEqual(expected_object, 'Готовченко')

