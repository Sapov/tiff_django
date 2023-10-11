import os
from datetime import date
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from .tiff_file import Calculation, check_tiff, WorkWithFile

import logging

logger = logging.getLogger(__name__)


class FinishWork(models.Model):
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
    is_active = models.BooleanField(default=True, verbose_name="Активный")

    def __str__(self):
        return self.work

    class Meta:
        verbose_name_plural = "Финишные обработки"
        verbose_name = "Финишная обработка"


class Contractor(models.Model):
    name = models.CharField(max_length=100, verbose_name="Поставщик продукции")

    class Meta:
        verbose_name_plural = "Подрядчики"
        verbose_name = "Подрядчикии"
        ordering = ["name"]

    def __str__(self):
        return self.name


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
        max_length=100, help_text="За 1 м2", verbose_name="Стоимость печати в руб."
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
        return f"{self.name} - {self.type_print}"

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
    Contractor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="ЗАКАЗЧИК!!",
        default=1,
    )
    material = models.ForeignKey(
        "Material", on_delete=models.PROTECT, verbose_name="Материал", default="2"
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
    resolution = models.IntegerField(
        default=0,
        verbose_name="Разрешение",
        help_text="для баннера 72 dpi, для Пленки 150 dpi",
    )
    color_model = models.CharField(
        max_length=10,
        default="CMYK",
        verbose_name="Цветовая модель",
        help_text="Для корректной печати модель должна быть CMYK",
    )
    size = models.FloatField(default=0, verbose_name="Размер в Мб")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, blank=True, null=True
    )
    images = models.FileField(upload_to="image")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )  # date created
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Изменено"
    )  # date update
    FinishWork = models.ForeignKey(
        "FinishWork",
        on_delete=models.PROTECT,
        verbose_name="Финишная обработка",
        default=1,
    )
    Fields = models.ForeignKey(
        "Fields",
        on_delete=models.PROTECT,
        verbose_name="Поля вокруг изображения",
        default=1,
    )
    in_order = models.BooleanField(
        verbose_name="Позиция в заказе", default=0, blank=True, null=True
    )
    status_product = models.ForeignKey(
        "StatusProduct",
        on_delete=models.PROTECT,
        verbose_name="Статус файла",
        default=1,
    )

    def __str__(self):
        return f"{self.images}"

    def get_absolute_url(self):
        return reverse("files:myfiles")

    class Meta:
        verbose_name_plural = "Файлы"
        verbose_name = "Файл"

    def save(self, *args, **kwargs):
        """расчет и запись стоимости баннера"""

        # Сравниваем размеры с разрешением материала печати
        # Считаем стоимость печати
        download_file = WorkWithFile(self.images)  # , self.material.resolution_print

        self.color_model = download_file.color_mode()
        logger.info(f"self.color_model {self.color_model}")
        self.width, self.length, self.resolution = download_file.check_tiff()
        logger.info(f"Разрешение:  {self.resolution}")
        # RESIZE IMAGE
        # download_file.check_resolution(self.material.resolution_print)
        # download_file.compress_image(self.material.resolution_print)
        # RENAME IMAGES

        self.price = download_file.price_calculation(self.quantity, self.material.price)
        # Считаем финишку
        self.price += download_file.finish_wokrs(
            self.FinishWork.price
        )  # Добавляю стоимость финишной обработки

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


class Fields(models.Model):
    fields = models.CharField(max_length=255, verbose_name="Поля вокруг изображения")

    def __str__(self):
        return self.fields

    class Meta:
        verbose_name_plural = "Поля"
        verbose_name = "Поле вокруг печати"


class UploadArh(models.Model):
    path_file = models.FileField(upload_to="upload_arhive")
