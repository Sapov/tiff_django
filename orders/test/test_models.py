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

    def test_total_price_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field('total_price').null
        expected_null = True
        self.assertEqual(null, expected_null)

    def test_total_price_help_text(self):
        order = Order.objects.get(id=1)
        help_text = order._meta.get_field('total_price').help_text
        expected_help_text = 'Стоимость заказа'
        self.assertEqual(help_text, expected_help_text)

    def test_cost_total_price_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('cost_total_price').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_cost_total_price_verbose_name(self):
        order = Order.objects.get(id=1)
        verobose_name = order._meta.get_field('cost_total_price').verbose_name
        expected_verbose_name = 'Общая Себестоимость'
        self.assertEqual(verobose_name, expected_verbose_name)

    def test_cost_total_price_max_length(self):
        order = Order.objects.get(id=1)
        max_length = order._meta.get_field('cost_total_price').max_length
        expected_max_length = 10
        self.assertEqual(max_length, expected_max_length)

    def test_cost_total_price_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field('cost_total_price').null
        expected_null = True
        self.assertEqual(null, expected_null)

    def test_cost_total_price_help_text(self):
        order = Order.objects.get(id=1)
        help_text = order._meta.get_field('cost_total_price').help_text
        expected_help_text = 'Себестоимость заказа'
        self.assertEqual(help_text, expected_help_text)

    def test_cost_total_price_field_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('cost_total_price').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_organisation_payer_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('organisation_payer').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_organisation_payer_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name = order._meta.get_field('organisation_payer').verbose_name
        expected_verbose_name = 'Организация плательщик'
        self.assertEqual(verbose_name, expected_verbose_name)

    def test_organisation_payer_null(self):
        order = Order.objects.get(id=1)
        null = order._meta.get_field('organisation_payer').null
        expected_null = True
        self.assertEqual(null, expected_null)

    def test_organisation_payer_help_text(self):
        order = Order.objects.get(id=1)
        help_text = order._meta.get_field('organisation_payer').help_text
        expected_help_text = 'Выберите организацию плательщик'
        self.assertEqual(help_text, expected_help_text)

    def test_organisation_payer_field_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('organisation_payer').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_organisation_payer_field_default(self):
        order = Order.objects.get(id=1)
        default_field = order._meta.get_field('organisation_payer').default
        expected_default = 1
        self.assertEqual(default_field, expected_default)

    def test_paid_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name_field = order._meta.get_field('paid').verbose_name
        expected_verbose_name = 'Заказ оплачен'
        self.assertEqual(verbose_name_field, expected_verbose_name)

    def test_paid_default(self):
        order = Order.objects.get(id=1)
        default_field = order._meta.get_field('paid').default
        expected_default = False
        self.assertEqual(default_field, expected_default)

    def test_date_complete_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name_field = order._meta.get_field('date_complete').verbose_name
        expected_verbose_name = 'Дата готовности заказа'
        self.assertEqual(verbose_name_field, expected_verbose_name)

    def test_date_complete_help_text(self):
        order = Order.objects.get(id=1)
        help_text = order._meta.get_field('date_complete').help_text
        expected_help_text = 'Введите дату к которой нужен заказ'
        self.assertEqual(help_text, expected_help_text)

    def test_date_complete_field_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('date_complete').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_date_complete_field_null(self):
        order = Order.objects.get(id=1)
        null_field = order._meta.get_field('date_complete').null
        expected_null = True
        self.assertEqual(null_field, expected_null)

    def test_comments_field_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name_filed = order._meta.get_field('comments').verbose_name
        expected_verbose_name = 'Комментарии к заказу'
        self.assertEqual(verbose_name_filed, expected_verbose_name)

    def test_comments_field_blank(self):
        order = Order.objects.get(id=1)
        blank = order._meta.get_field('comments').blank
        expected_blank = True
        self.assertEqual(blank, expected_blank)

    def test_status_field_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name_filed = order._meta.get_field('status').verbose_name
        expected_verbose_name = 'Статус заказа'
        self.assertEqual(verbose_name_filed, expected_verbose_name)

    def test_status_field_default(self):
        order = Order.objects.get(id=1)
        default_field = order._meta.get_field('status').default
        expected_default = 1
        self.assertEqual(default_field, expected_default)

    def test_created_field_auto_now_add(self):
        order = Order.objects.get(id=1)
        auto_now_add_field = order._meta.get_field('created').auto_now_add
        expected_auto_now_add = True
        self.assertEqual(auto_now_add_field, expected_auto_now_add)

    def test_updated_field_auto_now(self):
        order = Order.objects.get(id=1)
        auto_now_field = order._meta.get_field('updated').auto_now
        expected_auto_now = True
        self.assertEqual(auto_now_field, expected_auto_now)

    def test_Contractor_verbose_name(self):
        order = Order.objects.get(id=1)
        verbose_name_field = order._meta.get_field('Contractor').verbose_name
        expected_verbose_name = 'Заказчик'
        self.assertEqual(verbose_name_field, expected_verbose_name)

    def test_Contractor_default_field(self):
        order = Order.objects.get(id=1)
        field = order._meta.get_field('Contractor').default
        expected = 1
        self.assertEqual(field, expected)

    def test_order_arhive_upload_to(self):
        order = Order.objects.get(id=1)
        field = order._meta.get_field('order_arhive').upload_to
        expected = f"arhive/{id}"
        self.assertEqual(field, expected)

    def test_order_arhive_null(self):
        order = Order.objects.get(id=1)
        field = order._meta.get_field('order_arhive').null
        expected = True
        self.assertEqual(field, expected)

    def test_order_arhive_blank(self):
        order = Order.objects.get(id=1)
        field = order._meta.get_field('order_arhive').blank
        expected = True
        self.assertEqual(field, expected)
