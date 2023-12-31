from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Дата рождения"
    )
    photo = models.ImageField(upload_to="users/%Y/%m/%d/", blank=True)
    phone = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Мобильный телефон"
    )
    telegram = models.CharField(max_length=15, blank=True, null=True)
    organisation = models.ForeignKey(
        "Organisation", on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return f"Profile of {self.user.username}"


class Organisation(models.Model):
    Contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="ЗАКАЗЧИК!!",
        default=1,
    )
    name_ul = models.CharField(
        max_length=70,
        verbose_name="Имя юр. лица",
        help_text="Форма собственности и название.Если платильщик физ. Лицо, оаставить физ. лицо. ",
        default='Физ. лицо'
    )
    address_ur = models.TextField(
        null=True,
        blank=True,
        verbose_name="Юр. Адрес",
        help_text="Полный почтовый адрес",
    )
    address_post = models.TextField(
        null=True, blank=True, verbose_name="Почтовый Адрес"
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    phone2 = models.CharField(
        max_length=20, blank=True, verbose_name="Телефон резервный"
    )
    email = models.EmailField(
        max_length=20, blank=True, verbose_name="Электронная почта"
    )
    inn = models.CharField(max_length=12, verbose_name="ИНН", blank=True)
    kpp = models.CharField(max_length=9, verbose_name="КПП", blank=True)
    okpo = models.CharField(max_length=12, blank=True, verbose_name="ОКПО")
    published = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Опубликовано"
    )

    # user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Организации"
        verbose_name = "Организация"
        ordering = ["name_ul"]

    def __str__(self):
        return self.name_ul


class Delivery(models.Model):
    type_delivery = models.CharField(max_length=200, verbose_name="Тип доставки", default=2)

    class Meta:
        verbose_name_plural = "Типы доставки"
        verbose_name = "Тип Доставки"
        ordering = ["type_delivery"]

    def __str__(self):
        return self.type_delivery


class DeliveryAddress(models.Model):
    city = models.CharField(max_length=200, verbose_name="Город")
    street = models.CharField(max_length=200, verbose_name="Улица")

    class Meta:
        verbose_name_plural = "Адреса доставки"
        verbose_name = "Адреса доставки"
        ordering = ["street"]

    def __str__(self):
        return self.street