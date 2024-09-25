from django.contrib.auth import get_user_model
from django.test import TestCase

from account.models import Delivery
from orders.models import BankInvoices, Order, StatusOrder

User = get_user_model()


class TestModelBankInvoices(TestCase):
    def setUp(self):
        BankInvoices.objects.create(order_id=1,
                                    document_id='2342342-234234-234',
                                    payment_Status='pament_true')

    def test_order_id_verbose_name(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('order_id').verbose_name
        expected_verbose_name = 'Номер заказа'
        self.assertEqual(name, expected_verbose_name)

    def test_document_id_verbose_name(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('document_id').verbose_name
        expected_verbose_name = 'Номер выставленного документа в банке'
        self.assertEqual(name, expected_verbose_name)

    def test_document_id_max_length(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('document_id').max_length
        expected_verbose_name = 40
        self.assertEqual(name, expected_verbose_name)

    def test_payment_Status_verbose_name(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('payment_Status').verbose_name
        expected_verbose_name = 'Статус оплаты'
        self.assertEqual(name, expected_verbose_name)

    def test_payment_Status_max_length(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('payment_Status').max_length
        expected_verbose_name = 40
        self.assertEqual(name, expected_verbose_name)

    def test_payment_Status_blank(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('payment_Status').blank
        expected_verbose_name = True
        self.assertEqual(name, expected_verbose_name)

    def test_payment_Status_null(self):
        invoice = BankInvoices.objects.get(id=1)
        name = invoice._meta.get_field('payment_Status').null
        expected_verbose_name = True
        self.assertEqual(name, expected_verbose_name)


class TestOrderModel(TestCase):
    def setUp(self):
        Delivery.objects.create(type_delivery='Паровозом')
        Order.objects.create(delivery=Delivery.objects.get(id=1),
                             cost_total_price=4,
                             organisation_payer=None,
                             paid=True,
                             date_complete=None,
                             comments='',
                             status=StatusOrder.objects.create(name='sdfsdf',
                                                               is_active=True),
                             Contractor=User.objects.create(username='Basa'), )

    def test_delivery_verbose_name(self):
        order = Order.objects.get(id=1)
        name = order._meta.get_field('delivery').verbose_name
        expected_verbose_name = 'Доставка'
        self.assertEqual(name, expected_verbose_name)

    def test_delivery_null(self):
        order = Order.objects.get(id=1)
        name = order._meta.get_field('delivery').null
        expected_null = True
        self.assertEqual(name, expected_null)

    def test_delivery_default(self):
        order = Order.objects.get(id=1)
        name = order._meta.get_field('delivery').default
        expected_default = 3
        self.assertEqual(name, expected_default)

    def test_total_price_verbose_name(self):
        order = Order.objects.get(id=1)
        verobose_name = order._meta.get_field('total_price').verbose_name
        expected_verbose_name = 'Общая Стоимость'
        self.assertEqual(verobose_name, expected_verbose_name)

    def test_total_price_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('total_price').max_length
        expected_max_length = 10
        self.assertEqual(max_length, expected_max_length)

    def test_total_price_max_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field('total_price').null
        expected_null = True
        self.assertEqual(null, expected_null)

    def test_total_price_help_text(self):
        order = Order.objects.get(id=1)
        help_text = order._meta.get_field('total_price').help_text
        expected_help_text = 'Стоимость заказа'
        self.assertEqual(help_text, expected_help_text)

    def test_total_price_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('total_price').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)