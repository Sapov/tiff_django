from django.test import TestCase
from files.tiff_file import Calculator

class TestCalculator(TestCase):

    dict_param = {'quantity': 1,
                  'material': 'material',
                  'finishing': 'FinishWork',
                  'length': 2.7,
                  'width': 0.8,
                  'role': 'CUSTOMER_RETAIL'}
    def setUp(self):
        item= Calculator

    def test_cal(self):
        pass

