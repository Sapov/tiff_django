import phonenumbers
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from account.views import Users


class Channel(models.TextChoices):
    WHATSAPP = "WHATSAPP", "whatsapp"  # розничный клиент
    TELEGRAM = "TELEGRAM", "telegram"  # розничный клиент
    EMAIL = 'EMAIL', 'email'
    PHONE = 'PHONE', 'Телефонный звонок'


class Interest(models.Model):
    name = models.CharField(max_length=255, verbose_name='Интерес')


class Lids(models.Model):
    name = models.CharField(verbose_name='Name')
    email = models.EmailField(auto_created='Email')
    phone_number = PhoneNumberField(blank=True, verbose_name='Номер телефона', help_text='В формате +7 953 119-33-67',
                                    null=True)

    channel = models.CharField(Cmax_length=64, choices=Channel.choices, default=Channel.PHONE,
                               verbose_name='Канал продаж')
    interest = models.ForeignKey(Interest, on_delete=models.PROTECT, verbose_name='Интерес')
    interest_text = models.TextField(verbose_name='Дополнительная информация')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='Владелиц лида')
