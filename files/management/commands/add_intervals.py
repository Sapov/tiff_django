from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule


# ___________________________________________________
# How import >> python manage.py add_intervals
# ___________________________________________________
class Command(BaseCommand):
    help = "Добавляем интервалы"

    def handle(self, *args, **options):
        # заполняем Типы материалов в таблицу TypePrint
        print('[INFO] Добавляем интервалы для Celery beat')
        print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ ЧАС ', "*" * 20)
        IntervalSchedule.objects.get_or_create(every=1, period='hours')
        print('*' * 20, 'ПОВТОРЕНИЕ ЧЕРЕЗ 2 МИНУТЫ ', "*" * 20)
        IntervalSchedule.objects.get_or_create(every=2, period='minutes')  # for test
