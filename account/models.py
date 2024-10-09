from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


class Organisation(models.Model):
    name_full = models.CharField(max_length=200, verbose_name="Имя юр. лица", help_text="Форма собственности и название")
    inn = models.CharField(max_length=12, verbose_name="ИНН")
    kpp = models.CharField(max_length=9, blank=True, verbose_name="КПП")
    address = models.CharField(max_length=256, verbose_name="Юр. Адрес", help_text="Полный почтовый адрес", )
    bank_account = models.CharField(max_length=20, verbose_name='Расчетный счет', null=True, blank=True, )
    bank_name = models.CharField(max_length=120, verbose_name='Название Банка', null=True, blank=True, )
    bik_bank = models.CharField(max_length=9, verbose_name='БИК Банка', null=True, blank=True, )
    bankCorrAccount = models.CharField(max_length=20, verbose_name='Кор.счет', null=True, blank=True, )
    address_post = models.CharField(max_length=256, null=True, blank=True, verbose_name="Почтовый Адрес")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(max_length=20, blank=True, verbose_name="Электронная почта")
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")


    class Meta:
        verbose_name_plural = "Организации"
        verbose_name = "Организация"
        ordering = ["name_full"]

    def __str__(self):
        return self.name_full


class Delivery(models.Model):
    type_delivery = models.CharField(
        max_length=200, verbose_name="Тип доставки", default=2
    )

    class Meta:
        verbose_name_plural = "Типы доставки"
        verbose_name = "Тип Доставки"
        ordering = ["type_delivery"]

    def __str__(self):
        return self.type_delivery


class DeliveryAddress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="ЗАКАЗЧИК!!", null=True, blank=True
    )
    region = models.CharField(
        max_length=100, verbose_name="Область", null=True, blank=True
    )

    city = models.CharField(max_length=200, verbose_name="Город", null=True, blank=True)
    street = models.CharField(
        max_length=200, verbose_name="Улица", null=True, blank=True
    )
    house = models.CharField(max_length=200, verbose_name="Дом", null=True, blank=True)
    entrance = models.CharField(
        max_length=10, verbose_name="Подъезд", null=True, blank=True
    )
    floor = models.CharField(max_length=10, verbose_name="Этаж", null=True, blank=True)
    flat = models.CharField(
        max_length=10, verbose_name="Квартира/офис", null=True, blank=True
    )

    first_name = models.CharField(
        max_length=100, verbose_name="Имя", null=True, blank=True
    )
    second_name = models.CharField(
        max_length=100, verbose_name="Фамилия", null=True, blank=True
    )
    phone = models.CharField(
        max_length=100, verbose_name="Телефон", null=True, blank=True
    )
    delivery_method = models.ForeignKey(
        Delivery,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Тип доставки",
        default=2,
    )

    class Meta:
        verbose_name_plural = "Адреса доставки"
        verbose_name = "Адреса доставки"
        ordering = ["street"]

    def __str__(self):
        return f"{self.delivery_method}-{self.city}-{self.street}-{self.house}"
