from django.core.management.base import BaseCommand
from files.models import StatusProduct, TypePrint, Fields, FinishWork
from orders.models import StatusOrder
from account.models import Delivery, DeliveryAddress
from .data_test import StatusProducts_data, TypePrint_data, Fields_data, FinishWork_data, StatusOrder_data, \
    Delivery_type_data


# ___________________________________________________
# How import >>
# STEP 1: python manage.py add_test_data && python manage.py add_price

# ___________________________________________________
class Command(BaseCommand):
    help = "Наполнить БД"

    # def handle(self, *args, **options):
    #     for status in StatusProducts_data:
    #         StatusProduct.objects.get_or_create(status=status)

        # # заполняем таблицу типы печати
        # for type_print in TypePrint_data:
        #     TypePrint.objects.get_or_create(type_print=type_print)

        # заполняем таблицу типы доставки
        # for type_delivery in Delivery_type_data:
        #     Delivery.objects.get_or_create(type_delivery=type_delivery)

        # for fields in Fields_data:
        #     Fields.objects.get_or_create(fields=fields)

        # for name in StatusOrder_data:
        #     StatusOrder.objects.get_or_create(name=name)
        #
        # for item in FinishWork_data:
        #     FinishWork.objects.get_or_create(
        #         work=item[0],
        #         price_contractor=item[1],
        #         price=item[2],
        #         price_customer_retail=item[3]
        #
        #     )

# class Command(BaseCommand):
#     def handle(self, *args, **options):
#         with open("price.csv", 'r', encoding="utf-8") as file:
#             for line in file:
#                 element = line.split(",")
#                 models.Ingredient.objects.get_or_create(name=element[0], measurement_unit=element[1])
