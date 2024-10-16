import os
from pathlib import Path

from django.urls import reverse_lazy
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "easy_thumbnails",
    "account.apps.AccountConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "files.apps.FilesConfig",
    "orders.apps.OrdersConfig",
    "users",
    "crispy_forms",
    "crispy_bootstrap4",
    'info',
    'rest_framework',
    "phonenumber_field",
    'django_extensions',
    'django_celery_beat',
    'delivery_in_bus',

]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap4"
CRISPY_TEMPLATE_PACK = "bootstrap4"
# _____________________LOGING________________________________
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {"format": "%(name)-12s %(levelname)-8s %(message)s"},
        "file": {"format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "console"},
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "file",
            "filename": "debug.log",
        },
    },
    "loggers": {"": {"level": "INFO", "handlers": ["console", "file"]}},
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mysite.wsgi.application"

DATABASES = {"default":
    {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
# ______________________POSTGRES_______________
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": "db01",
#         "USER": os.getenv("POSTGRES_USER"),
#         "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
#         "HOST": os.getenv("POSTGRES_HOST"),
#         "PORT": os.getenv("POSTGRES_PORT"),
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ru-ru"

TIME_ZONE = "Europe/Moscow"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = "static"
STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

AUTH_USER_MODEL = "users.User"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
MEDIA_URL = "/media/"
# MEDIA_ROOT = BASE_DIR / "media"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
LOGIN_REDIRECT_URL = "account:dashboard"
LOGIN_URL = "login"
# LOGOUT_URL = "logout"
LOGOUT_URL = reverse_lazy('logout')

LOGOUT_REDIRECT_URL = 'login'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
EMAIL_USE_SSL = False

# # ---------------------CELERY-------------------------
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
# CELERY_BROKER_URL = 'redis://redis:6379/0'
# CELERY_RESULT_BACKEND = 'redis://redis:6379/0'

CELERY_IMPORTS = [
    'orders.tasks',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',  # web Отображение

    ],

}
PHONENUMBER_DEFAULT_REGION = 'RU'

CSRF_TRUSTED_ORIGINS = []
if scrf_subdomain := os.getenv('SCRF_SUBDOMAIN'):
    CSRF_TRUSTED_ORIGINS += [f'http://{scrf_subdomain}', f'https://{scrf_subdomain}']
