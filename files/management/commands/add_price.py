from django.core.management.base import BaseCommand
from files.models import Material
from orders.models import StatusOrder
from .data_price import Material_data


#___________________________________________________
# How import >> python manage.py add_test_data
#___________________________________________________
class Command(BaseCommand):
    help = "Наполнить - прайс"

    def handle(self, *args, **options):
        for item in Material_data:
            Material.objects.get_or_create(
                name=item[0],
                type_print=item[1],
                price_contractor=item[2],
                price=item[3],
                resolution_print=item[4]

            )
