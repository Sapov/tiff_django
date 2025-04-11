from django.test import TestCase

from orders.payment.New_bank import Bank



class TestClassBank(TestCase):


    def test_urls(self):
        url = Bank.url
        expected_url = 'https://enter.tochka.com/uapi/invoice/v1.0/bills'
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    a = TestClassBank()
    a.test_urls()