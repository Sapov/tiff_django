from django.core.management.base import BaseCommand
from files.models import StatusProduct, TypePrint, Fields, FinishWork, Material
from .data_test import StatusProducts_data, TypePrint_data, Fields_data, FinishWork_data, Material_data


class Command(BaseCommand):
    help = "Наполнить БД"

    def handle(self, *args, **options):
        for status in StatusProducts_data:
            StatusProduct.objects.get_or_create(status=status)

        for type_print in TypePrint_data:
            TypePrint.objects.get_or_create(type_print=type_print)

        for fields in Fields_data:
            Fields.objects.get_or_create(fields=fields)

        for fields in Fields_data:
            Fields.objects.get_or_create(fields=fields)

        for item in FinishWork_data:
            FinishWork.objects.get_or_create(
                work=item[0],
                price_contractor=item[1],
                price=item[2]

            )
        # for item in Material_data:
        #     Material.objects.get_or_create(
        #         name=item.get('name'),
        #         type_print=item.get('type_print'),
        #         price_contractor=item.get('price_contractor'),
        #         price=item.get('price'),
        #         resolution_print=item.get('resolution_print')
        #
        #     )
