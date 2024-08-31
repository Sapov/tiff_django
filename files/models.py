import os
from datetime import date
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from .tiff_file import check_tiff, WorkWithFile, Calculator

import logging

logger = logging.getLogger(__name__)


class FinishWork(models.Model):
    ''' финищная обработка'''
    work = models.CharField(max_length=255, verbose_name="Финишная обработка")
    price_contractor = models.FloatField(
        max_length=100,
        help_text="Цена за 1 м. погонный",
        verbose_name="Себестоимость работы в руб.",
        blank=True,
        null=True,
        default=None,
    )  # стоимость в закупке
    price = models.FloatField(
        max_length=100,
        help_text="Цена за 1 м. погонный",
        verbose_name="Стоимость работы в руб.",
    )

    price_customer_retail = models.FloatField(
        max_length=100,
        help_text="Цена за 1 м. погонный",
        verbose_name="Стоимость работы розница в руб.",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True, verbose_name="Активный")

    def __str__(self):
        return self.work

    class Meta:
        verbose_name_plural = "Финишные обработки"
        verbose_name = "Финишная обработка"


class Contractor(models.Model):
    '''Организации исполнители работ'''
    name = models.CharField(max_length=100, verbose_name="Наименование организации")
    description = models.CharField(max_length=200, verbose_name="Описание направления деятельности")
    email_contractor = models.EmailField(verbose_name="Email организации")
    phone_contractor = models.CharField(max_length=11, verbose_name="Телефон организации")
    phone_contractor_2 = models.CharField(max_length=11, verbose_name="Телефон организации")
    address = models.CharField(verbose_name="Адрес", max_length=200)
    contact_contractor = models.CharField(max_length=23, verbose_name="Контактное лицо")

    class Meta:
        verbose_name_plural = "Подрядчики"
        verbose_name = "Подрядчикии"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("files:contractor_view")


class TypePrint(models.Model):
    type_print = models.CharField(max_length=128, verbose_name="Метод печати")
    info_type_print = models.TextField(verbose_name="Описание метода печати")

    class Meta:
        verbose_name_plural = "Типы печати"
        verbose_name = "Тип печати"
        ordering = ["type_print"]

    def __str__(self):
        return self.type_print


class Material(models.Model):
    name = models.CharField(
        max_length=100,
        help_text="Введите имя материала для печати",
        verbose_name="Материал для печати",
        blank=True,
        null=True,
        default=None,
    )
    type_print = models.ForeignKey(
        TypePrint,
        on_delete=models.PROTECT,
        verbose_name="Тип печати",
        blank=True,
        null=True,
        default=None,
    )
    price_contractor = models.FloatField(
        max_length=100,
        help_text="За 1 м2",
        verbose_name="Себестоимость печати в руб.",
        blank=True,
        null=True,
        default=None,
    )  # стоимость в закупке
    price = models.FloatField(
        max_length=100,
        help_text="За 1 м2",
        verbose_name="Стоимость печати для РА в руб.",
    )
    price_customer_retail = models.FloatField(
        max_length=100,
        help_text="За 1 м2",
        verbose_name="Стоимость печати розница в руб.",
        null=True,
        blank=True,
    )
    resolution_print = models.IntegerField(
        help_text="разрешение для печати на материале",
        verbose_name="DPI",
        blank=True,
        null=True,
        default=None,
    )
    is_active = models.BooleanField(default=True, verbose_name="Активный ")

    def __str__(self):
        return f"{self.name} {self.type_print}"

    class Meta:
        verbose_name_plural = "Материалы для печати"
        verbose_name = "Материал"
        ordering = ["name"]


class StatusProduct(models.Model):
    status = models.CharField(max_length=64, verbose_name="Статус файла")

    def __str__(self):
        return f"{self.status}"

    class Meta:
        verbose_name_plural = "Статусы файлов"
        verbose_name = "Статус файла"


class Product(models.Model):
    objects = None
    Contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="ЗАКАЗЧИК!!",
        default=1,
    )
    material = models.ForeignKey("Material", on_delete=models.PROTECT, verbose_name="Материал")
    quantity = models.IntegerField(default=1, help_text="Введите количество", verbose_name="Количество")
    width = models.FloatField(default=0, verbose_name="Ширина", help_text="Указывается в см.")
    length = models.FloatField(default=0, verbose_name="Длина", help_text="Указывается в см.")
    resolution = models.IntegerField(default=0, verbose_name="Разрешение", help_text="для баннера"
                                                                                     "72 dpi, для Пленки 150 dpi", )
    color_model = models.CharField(max_length=10, default="CMYK", verbose_name="Цветовая модель",
                                   help_text="Для корректной печати модель должна быть CMYK", )
    size = models.FloatField(default=0, verbose_name="Размер в Мб")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    images = models.FileField(upload_to="image", verbose_name="Загрузка файла")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update
    FinishWork = models.ForeignKey("FinishWork",
                                   on_delete=models.PROTECT,
                                   verbose_name="Финишная обработка",
                                   default=1,
                                   )

    in_order = models.BooleanField(verbose_name="Позиция в заказе", default=0, blank=True, null=True)
    status_product = models.ForeignKey(
        "StatusProduct",
        on_delete=models.PROTECT,
        verbose_name="Статус файла",
        default=1,
    )
    comments = models.TextField(verbose_name="Комментарии к файлу", blank=True, null=True)

    def __str__(self):
        return f"{self.images}"

    def get_absolute_url(self):
        return reverse("files:myfiles")

    class Meta:
        verbose_name_plural = "Файлы"
        verbose_name = "Файл"

    def save(self, *args, **kwargs):
        """Расчет и запись стоимости баннера"""

        # Сравниваем размеры с разрешением материала печати
        # Считаем стоимость печати
        download_file = WorkWithFile(self.images)  # , self.material.resolution_print

        self.color_model = (download_file.color_mode())  # Цветовая модель if request.user.role == "CUSTOMER_RETAIL":

        logger.info(f"Цветовая модель: {self.color_model}")
        self.width, self.length, self.resolution = download_file.check_tiff()
        logger.info(f"Разрешение:  {self.resolution}")
        # RESIZE IMAGE
        # download_file.check_resolution(self.material.resolution_print)
        # download_file.compress_image(self.material.resolution_print)
        # RENAME IMAGES
        # 0-------------------class
        image_parameters = Calculator(self.width, self.length, self.Contractor.role, self.material, self.FinishWork,
                                      self.quantity)
        self.price = image_parameters.calculate()
        # -----------

        # СЕБЕСТОИМОСТЬ
        self.cost_price = download_file.price_calculation(
            self.quantity, self.material.price_contractor
        )
        logger.info(f"Себестоимость: self.cost_price {self.cost_price}")
        self.cost_price += download_file.finish_wokrs(
            self.FinishWork.price_contractor
        )  # Добавляю стоимость финишной обработки
        logger.info(f"Себестоимость: с финишкой {self.cost_price}")

        super(Product, self).save(*args, **kwargs)


def product_post_save(sender, instance, created, **kwargs):
    material = instance.material
    resolution = instance.resolution
    images = instance.images
    # Сравниваем размеры с разрешением материала печати
    # WorkWithFile.check_resolution(material, resolution, images)


post_save.connect(product_post_save, sender=Product)


class UploadArh(models.Model):
    path_file = models.FileField(upload_to="upload_arhive")


class UseCalculator(models.Model):
    ''' Расчеты пользователей сайта '''

    material = models.ForeignKey(
        "Material", on_delete=models.PROTECT, verbose_name="Материал"
    )
    quantity = models.IntegerField(
        default=1, help_text="Введите количество", verbose_name="Количество"
    )
    width = models.FloatField(
        default=0, verbose_name="Ширина", help_text="Указывается в см."
    )
    length = models.FloatField(
        default=0, verbose_name="Длина", help_text="Указывается в см."
    )

    results = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, verbose_name="Стоимость")

    FinishWork = models.ForeignKey(
        "FinishWork",
        on_delete=models.PROTECT,
        verbose_name="Финишная обработка",
        default=1)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )

    def __str__(self):
        return f'Дата: {str(self.created_at)[:16]} /{str(self.material)[:10]}/ Кол-во: {self.quantity}шт./Размер: {self.width}x{self.length}м./Стоимость: {self.results} руб.'

    class Meta:
        verbose_name_plural = "Расчеты клиентов сайта"
        verbose_name = "Расчет клиентов сайта"
