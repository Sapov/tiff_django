from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule

from files.models import Material, FinishWork, TypePrint, StatusProduct
from lids.models import Interest
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

        '''заполняем ширку из первого  листа с диапазоном b2:f11 '''
        print('*' * 30, 'Заполняю базу стоимости Широкоформатная печать материалов из файла', '*' * 30)
        for item in load_excel('shirka', 'b2:e11'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=1)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
            )
        '''заполняем стоимость пустого материала диапазоном b2:E9 '''
        print('*' * 30, 'Заполняю базу стоимости Пустого материала из файла', '*' * 30)
        for item in load_excel('blank_material', 'b2:E9'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=4)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
            )

        print('*' * 30, 'Заполняю базу стоимости Интерьерку печать материалов из файла', '*' * 30)
        for item in load_excel('interierka', 'b2:e17'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=2)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
            )

        print('*' * 30, 'Заполняю базу стоимости UV print печать материалов ', '*' * 30)
        for item in load_excel('uf-print', 'b2:e18'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=3)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
            )
        print('*' * 30, 'Заполняю базу стоимости печати картин на холсте ', '*' * 30)
        for item in load_excel('picturies', 'b2:e13'):
            print(item)
            Material.objects.get_or_create(
                name=item[0],
                type_print=TypePrint.objects.get_or_create(id=5)[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
            )

        # заполняем Финишку в таблицу FinishWork
        print('*' * 30, 'Заполняю Постпечатную обработку', '*' * 30)
        for item in load_excel('finishka', 'b2:e11'):
            print(item)
            FinishWork.objects.get_or_create(
                work=item[0],
                price_contractor=item[1],
                price=item[2],
                price_customer_retail=item[3],
                # is_active=item[4]
            )

    # def _load_items_one_field(self, sheet: str, range_cell: str, model: str, anotation: str, field: str):
    #     print('*' * 30, anotation, '*' * 30)
    #     '''Загружаю данные в базу'''
    #     for item in load_excel(sheet, range_cell):
    #         print(item)
    #         model.objects.get_or_create(field=item[0])
    #
    # _load_items_one_field('status_product',
    #                       'b2:b4',
    #                       'StatusProduct',
    #                       'заполняем Статус Продукта ',
    #                       'status')

        print('*' * 30, 'заполняем Статус Продукта ', '*' * 30)
        for status in load_excel('status_product', 'b2:b5'):
            print(status)
            StatusProduct.objects.get_or_create(status=status[0])

        print('*' * 30, 'заполняем Статус Заказа ', '*' * 30)
        for status in load_excel('status_order', 'b2:b6'):
            print(status)
            StatusOrder.objects.get_or_create(name=status[0])
        # _load_items_one_field('status_order',
    #                            'b2:b6',
    #                            'StatusOrder',
    #                            'заполняем Статус Заказа ',
    #                            'status')


        print('*' * 30, 'заполняем Интересы лидов ', '*' * 30)
        for name in load_excel('Interest', 'b2:b9'):
            print(name)
            Interest.objects.get_or_create(name=name[0])


def add_intervals_for_celery_beat(self):
    print('[INFO] Добавляем интервалы для Celery beat')
    print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ ЧАС ', "*" * 20)
    IntervalSchedule.objects.create(every=1, period='hours')
    print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ 2 МИНУТЫ ', "*" * 20)
    IntervalSchedule.objects.get(every=2, period='minutes')  # for test
