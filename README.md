# tiff_django
 CMS проверки файла на django + easy_thumbnails
![action status](https://github.com/Sapov/tiff_django/actions/workflows/django.yml/badge.svg)

Для ручной установки:
1. Выполняем миграции
>> python manage.py migrate
2. Добавляем админа 
>> python manage.py createsuperuser

1. Заполняем базу даннымим:
>> python manage.py add_test_data
2. Заполняем прайс лист
>> python manage.py add_test_data

как запустить git clone
docker compose up

Остановить: docker compose down
Сейчас запускаю на 88 порту: указывается в .env