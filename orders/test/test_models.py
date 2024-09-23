from django.test import TestCase

from orders.models import BankInvoices


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
