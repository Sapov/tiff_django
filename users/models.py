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
    phones = PhoneNumberField()

    email_verify = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
