# tiff_django
 CMS проверки файла на django + easy_thumbnails
![action status](https://github.com/Sapov/tiff_django/actions/workflows/django.yml/badge.svg)

Как запустить: 
1. git clone
2. Создать .env
3. docker compose up
4. Зайти в docker django
5. Добавить админа (сменю скоро на дефолтного) -> изменить пароль с admin/admin
   
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

#--------------для генерации счета-----------------

BANK_NAME="имя банка" 

BIK_NUMBER=Бик номер 

ORDER_KOR='Кор. счет'

INN='инн номер'

NUM_ORDER='номер счета'

NAME_ORGANISATION='Название оранизации'

ADDRESS_1='Юр. Адрес'

ADDRESS_2='Почтовый Адрес'

_____________________________________________________


Остановить: docker compose down
