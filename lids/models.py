from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.urls import reverse

from account.views import Users


class Channel(models.TextChoices):
    WHATSAPP = "WHATSAPP", "whatsapp"  # розничный клиент
    TELEGRAM = "TELEGRAM", "telegram"  # розничный клиент
    EMAIL = 'EMAIL', 'email'
    PHONE = 'PHONE', 'Телефонный звонок'
    SITE = 'SITE', 'Сайт'


class LidStatus(models.TextChoices):
    ANSWER = 'ANSWER', 'Ответил на вопросы'
    POSTING = 'POSTING', 'выслал дополнительную информацию'
    DESIGN_HOW = 'DESIGN_HOW', 'Отослал дизайнер для расчета'
    DESIGN = 'DESIGN', 'Разработка макета'
    ORDER = 'ORDER', 'Выставление счета'
    PRODUCTION = 'PRODUCTION', 'В работе'
    COMPLETE = 'COMPLETE', 'Cообщили о готовности'
    FEEDBACK = 'FEEDBACK', 'Отсылаем просьбу об отзыве'


class Interest(models.Model):
    name = models.CharField(max_length=255, verbose_name='Интерес')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Интересы'
        verbose_name = 'Интерес'


class Lids(models.Model):
    lid_status = models.CharField(max_length=64, choices=LidStatus.choices, default=LidStatus.ANSWER,
                                  verbose_name='Статус лида', db_default='DESIGN')
    username = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True)
    email = models.EmailField(verbose_name='Почта', blank=True, null=True)
    phone = PhoneNumberField(blank=True, verbose_name='Номер телефона', help_text='В формате +7 953 119-33-67',
                                    null=True)
    channel = models.CharField(max_length=64, choices=Channel.choices, default=Channel.SITE,
                               verbose_name='Канал продаж')
    interest = models.ForeignKey(Interest, on_delete=models.PROTECT, verbose_name='Тема сообщения', default=1)
    interest_text = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")
    update_at = models.DateTimeField(auto_now=True, verbose_name='Изменено')
    user = models.ForeignKey(  # переименовать в юзера!!!!!
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелиц лида",

    )

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        print(self.user)

        return reverse("lids:list_lids")
        # return reverse("lids:list_lids", args=[self.id])

    class Meta:
        verbose_name_plural = 'Лиды'
        verbose_name = 'Лид'
        ordering = ['-created_at']
