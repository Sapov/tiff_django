from django.test import TestCase


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
