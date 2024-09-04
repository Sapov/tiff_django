from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import os
User = get_user_model()


class Command(BaseCommand):
    USER_NAME = os.getenv('USER_NAME')
    USER_MAIL = os.getenv('USER_MAIL')
    USER_PASSWORD = os.getenv('USER_PASSWORD')

    def handle(self, *args, **options):
        print('[INFO] Добавляю супер пользователя:', self.USER_NAME, '\n',
              )
        User.objects.create_superuser(username=self.USER_NAME, email=self.USER_MAIL, password=self.USER_PASSWORD)
