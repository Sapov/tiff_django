#!/bin/bash
echo '[INFO] --Создаем каталоги для файлов--'
mkdir media
mkdir media/orders
mkdir media/arhive

#DJANGO_SETTINGS_MODULE=mysite.settings_dev python3 manage.py makemigrations
#DJANGO_SETTINGS_MODULE=mysite.settings_dev python3 manage.py add_price
#DJANGO_SETTINGS_MODULE=mysite.settings_dev python3 manage.py add_intervals
#DJANGO_SETTINGS_MODULE=mysite.settings_dev python3 manage.py add_default_admin
uv run python manage.py makemigrations  --settings mysite.settings_dev
uv run python manage.py migrate  --settings mysite.settings_dev

echo 'Добавлю админа'
uv run python manage.py add_default_admin  --settings mysite.settings_dev
echo 'Загружаю цены в БД'
uv run  python manage.py add_price  --settings mysite.settings_dev
echo 'Добавляю интервалы для Celery'
uv run python manage.py add_intervals  --settings mysite.settings_dev


DJANGO_SETTINGS_MODULE=mysite.settings_dev celery -A mysite worker -l info
