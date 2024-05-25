from django.core.management.base import BaseCommand
from files.models import Material, FinishWork, TypePrint, StatusProduct
from orders.models import StatusOrder
from .from_excel import load_excel


# ___________________________________________________
# How import >> python manage.py add_price
# ___________________________________________________
class Command(BaseCommand):
    help = "Наполнить - прайс"

    def handle(self, *args, **options):
        '''заполняем ширку из первого  листа с диапазоном b2:f9 '''
        print('*' * 30, 'Заполняю базу стоимости Широкоформатная печать материалов из файла', '*' * 30)
        for item in load_excel('shirka', 'b2:f9'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=1)[0],
                price_contractor=item[1],
                price_agent=item[2],
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
                price_agent=item[2],
                price_customer_retail=item[3],
                # is_active=item[4]
            )
        # заполняем Типы материалов в таблицу TypePrint
        print('*' * 30, 'заполняем Типы материалов в таблицу TypePrint', '*' * 30)
        for type_print in load_excel('type_print', 'b2:b5'):
            print(type_print)
            TypePrint.objects.get_or_create(type_print=type_print)

        print('*' * 30, 'заполняем Статус Продукта ', '*' * 30)
        for status in load_excel('status_product', 'b2:b5'):
            StatusProduct.objects.get_or_create(status=status)

        print('*' * 30, 'заполняем Статус Заказа ', '*' * 30)
        for status in load_excel('status_order', 'b2:b6'):
            StatusOrder.objects.get_or_create(name=status)
