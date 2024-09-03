from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    USER_NAME = 'admin'
    USER_MAIL = 'admin@admin.ru'
    USER_PASSWORD = 'admin'

    def handle(self, *args, **options):
        print('[INFO] Добавляю супер пользователя:', self.USER_NAME, '\n',
              )
        User.objects.create_superuser(username=self.USER_NAME, email=self.USER_MAIL, password=self.USER_PASSWORD)
