from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Role(models.TextChoices):
    '''Роли пользователей'''
    CUSTOMER = 'CUSTOMER', 'Клиент'
    MANAGER = 'MANAGER', 'Менеджер'
    OPERATOR = 'OPERATOR', 'Оператор'
    FINANCIER = 'FINANCIER', 'Бухгалтер'


class User(AbstractUser):
    role = models.CharField(
        max_length=24,
        choices=Role.choices,
        default=Role.CUSTOMER)
    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
