# tiff_django


Как запустить: 
git clone https://github.com/Sapov/tiff_django.git

ЛОКАЛЬНО:

PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=mysite.settings_dev python3 manage.py runserver
docker run -d -p 6379:6379  redis      
DJANGO_SETTINGS_MODULE=mysite.settings_dev celery -A mysite worker -l info

DJANGO_SETTINGS_MODULE=mysite.settings_dev celery -A mysite beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler



---------------- .env ---------------------------------

POSTGRES_HOST=(postgres_db) - такой же как в docker compose (container_name: postgres_db)

POSTGRES_PORT=(5432) - по умолчанию 

POSTGRES_USER=(postgres user) 

POSTGRES_PASSWORD=(postgres password)

POSTGRES_DB=(db01 - name DB)

NGINX_EXTERNAL_PORT=(порт nginx по умолчанию: 80) 

DJANGO_SETTINGS_MODULE=mysite.settings (настройки django)

EMAIL_HOST=(smtp.gmail.com) - настройка почтового сервера

EMAIL_HOST_USER=user_mail@gmail.com

EMAIL_HOST_PASSWORD=userPaSsWoRd 

EMAIL_PORT=(587 - для порт для google почты)

EMAIL_USE_TLS=True


SECRET_KEY='SecRet_Key' 


Остановить: docker compose down

Локально:
python manage.py runserver --settings mysite.settings_dev

Запускаем redis:
docker run -d -p 6379:6379 redis

Запускаем Celery:
DJANGO_SETTINGS_MODULE=mysite.settings_dev celery -A mysite worker -l info
