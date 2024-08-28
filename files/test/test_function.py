import logging
from unittest import TestCase
import datetime

from orders.views import select_time_complete


class TestFunctionSelectTimeComplete(TestCase):
    '''Тестрование функции расчета времени готовности заказа'''
    def test_select_data_complete_four_day(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 8, 29, )), '2024-09-02')

    #     pass
    def test_select_data_complete_one_day(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 8, 28, )), '2024-08-30')

    def test_select_data_complete_five_day(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 8, 30)), '2024-09-02')

    def test_select_data_complete_six_day(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 8, 31)), '2024-09-03')

    def test_select_complete_seven_day(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 8, 25)), '2024-08-27')

    def test_select_data_complete_28_february(self):
        self.assertEqual(select_time_complete(datetime.datetime(2024, 2, 28)), '2024-03-01')
        self.assertEqual(select_time_complete(datetime.datetime(2025, 2, 28)), '2025-03-03')

#
# def select_time_complete(today):
#     ''' Выбор времени готовности заказа'''
#     print('TYPE', today, type(today))
#     print('Это день недели', {today.isoweekday()})
#     logging.info(f"[ДАТА ГОТОВНОСТИ + ДВА ДНЯ К ДАТЕ ЗАКАЗА] {today.isoweekday()}")
#     # Если заказ приняли в четверг, то отдадим только в понедельник
#     if today.isoweekday() == 4:
#         # + 4 дня так как два выходных
#         today = today + datetime.timedelta(days=4)
#         # Оформленный в пятницу будет готов в понедельник
#     elif today.isoweekday() == 5 or today.isoweekday() == 6:
#         today = today + datetime.timedelta(days=3)
#     # Оформленный заказ в субботу готов будет во вторник + 3
#     # Оформленный заказ в воскресенье готов во вторник + 2
#     else:
#         today = today + datetime.timedelta(days=2)
#     today = today.strftime("%Y-%m-%d")
#     return today


# if __name__ == '__main__':
#     print(select_time_complete(today=datetime.datetime.today()))
