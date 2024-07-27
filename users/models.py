from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Role(models.TextChoices):
    """Роли пользователей"""

    CUSTOMER_RETAIL = "CUSTOMER_RETAIL", "Клиент"  # розничный клиент
    CUSTOMER_AGENCY = "CUSTOMER_AGENCY", "Рекламное агентство"  # Рекламное агентство
    MANAGER = "MANAGER", "Менеджер"
    OPERATOR = "OPERATOR", "Оператор"
    FINANCIER = "FINANCIER", "Бухгалтер"


class User(AbstractUser):
    role = models.CharField(
        max_length=24, choices=Role.choices, default=Role.CUSTOMER_RETAIL
    )
    email = models.EmailField(_("email address"), unique=True, )
    email_verify = models.BooleanField(default=False)
    phone_number = PhoneNumberField(blank=True, verbose_name='Номер телефона', help_text='В формате +7 953 119-33-67',
                                    null=True)
    whatsapp = models.BooleanField(verbose_name='Whatsapp', help_text='На телефоне установлен whatsapp', null=True,
                                   blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
