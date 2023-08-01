from django.core.management.base import BaseCommand
from files.models import StatusProduct, TypePrint, Fields, FinishWork, Material
from orders.models import StatusOrder
from .data_test import StatusProducts_data, TypePrint_data, Fields_data, FinishWork_data, StatusOrder_data, \
    Material_data


#___________________________________________________
# How import >> python manage.py add_test_data
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
        for item in Material_data:
            Material.objects.get_or_create(
                name=item[0],
                type_print=item[1],
                price_contractor=item[2],
                price=item[3],
                resolution_print=item[4]

            )
