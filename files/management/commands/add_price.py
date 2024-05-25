from django.core.management.base import BaseCommand

from account.models import Delivery
from files.models import Material, FinishWork, TypePrint, StatusProduct
from orders.models import StatusOrder
from .from_excel import load_excel


# ___________________________________________________
# How import >> python manage.py add_price
# ___________________________________________________
class Command(BaseCommand):
    help = "Наполнить - прайс"

    def handle(self, *args, **options):
        # заполняем Типы материалов в таблицу TypePrint
        print('*' * 30, 'заполняем Типы материалов в таблицу TypePrint', '*' * 30)
        for type_print in load_excel('type_print', 'b2:b5'):
            print(type_print)
            TypePrint.objects.get_or_create(type_print=type_print[0])

        '''заполняем ширку из первого  листа с диапазоном b2:f9 '''
        print('*' * 30, 'Заполняю базу стоимости Широкоформатная печать материалов из файла', '*' * 30)
        for item in load_excel('shirka', 'b2:f9'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=1)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
                resolution_print=item[4]
            )

        print('*' * 30, 'Заполняю базу стоимости Интерьерку печать материалов из файла', '*' * 30)
        for item in load_excel('interierka', 'b2:f17'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=2)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
                resolution_print=item[4]
            )

        print('*' * 30, 'Заполняю базу стоимости UV print печать материалов ', '*' * 30)
        for item in load_excel('uf-print', 'b2:f6'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=2)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
                resolution_print=item[4]
            )

        # заполняем Финишку в таблицу FinishWork
        print('*' * 30, 'Заполняю Постпечатную обработку', '*' * 30)
        for item in load_excel('finishka', 'b2:e8'):
            print(item)
            FinishWork.objects.get_or_create(
                work=item[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
                # is_active=item[4]
            )

        print('*' * 30, 'заполняем Статус Продукта ', '*' * 30)
        for status in load_excel('status_product', 'b2:b4'):
            print(status)
            StatusProduct.objects.get_or_create(status=status[0])

        print('*' * 30, 'заполняем Статус Заказа ', '*' * 30)
        for status in load_excel('status_order', 'b2:b6'):
            print(status)
            StatusOrder.objects.get_or_create(name=status[0])

        print('*' * 30, 'заполняем Типы доставки ', '*' * 30)
        for type_delivery in load_excel('delivery', 'b2:b2'):
            print(type_delivery)
            Delivery.objects.get_or_create(type_delivery=type_delivery[0])
