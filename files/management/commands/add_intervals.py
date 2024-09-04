from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule

from account.models import Delivery
from files.models import Material, FinishWork, TypePrint, StatusProduct
from orders.models import StatusOrder
from .from_excel import load_excel


# ___________________________________________________
# How import >> python manage.py add_intervals
# ___________________________________________________
class Command(BaseCommand):
    help = "Добавляем интервалы"

    def handle(self, *args, **options):
        # заполняем Типы материалов в таблицу TypePrint
        print('[INFO] Добавляем интервалы для Celery beat')
        print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ ЧАС ', "*" * 20)
        IntervalSchedule.objects.create(every=1, period='hours')
        print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ 2 МИНУТЫ ', "*" * 20)
        IntervalSchedule.objects.get(every=2, period='minutes')  # for test
