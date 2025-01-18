from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField

from files.models import Material


# Create your models here.
class SiteOrder(models.Model):
    # Таблица заявок с сайте через форму
    name = models.CharField(max_length=255, verbose_name='Имя', blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, verbose_name='Номер телефона', help_text='В формате +7 953 119-33-67',
                                    null=True)
    email = models.EmailField(max_length=255, verbose_name='Email', blank=True, null=True)
    material = models.ForeignKey(Material, on_delete=models.PROTECT, verbose_name='Материал для печати', blank=True,
                                 null=True)
    size_banner = models.CharField(max_length=255, verbose_name='Размер носителя', help_text='ширина Х высота в метрах',
                                   blank=True, null=True)
    info = models.TextField(verbose_name='Дополнительная информация', blank=True, null=True)

    def get_absolute_url(self):
        return reverse("bforms:order_complete")
