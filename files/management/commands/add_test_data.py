from django.core.management.base import BaseCommand
from files.models import StatusProduct, TypePrint, Fields, FinishWork
from orders.models import StatusOrder
from .data_test import StatusProducts_data, TypePrint_data, Fields_data, FinishWork_data, StatusOrder_data

#___________________________________________________
# How import >>
# STEP 1: python manage.py add_test_data
# STEP 2: python manage.py add_price
#___________________________________________________
class Command(BaseCommand):
    help = "Наполнить БД"

    def handle(self, *args, **options):
        for status in StatusProducts_data:
            StatusProduct.objects.get_or_create(status=status)

        for type_print in TypePrint_data:
            TypePrint.objects.get_or_create(type_print=type_print)

        for fields in Fields_data:
            Fields.objects.get_or_create(fields=fields)

        for name in StatusOrder_data:
            StatusOrder.objects.get_or_create(name=name)

        for item in FinishWork_data:
            FinishWork.objects.get_or_create(
                work=item[0],
                price_contractor=item[1],
                price=item[2]

            )
