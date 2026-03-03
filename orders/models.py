import logging
import os

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse

from profiles.models import Organisation, DeliveryAddress
from files.models import Product

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# from django.contrib.sites.models import Site

logger = logging.getLogger(__name__)
Image.MAX_IMAGE_PIXELS = None  # отключаем проверку разрешения


class StatusOrder(models.Model):
    name = models.CharField(max_length=48, verbose_name="Статус заказа")
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Статусы"
        verbose_name = "Статус"


class Order(models.Model):
    delivery = models.ForeignKey(DeliveryAddress, on_delete=models.PROTECT, verbose_name='Доставка', null=True, default=1)
    total_price = models.FloatField(max_length=10, null=True, help_text="Стоимость заказа",
                                    verbose_name="Общая Стоимость", blank=True, )
    cost_total_price = models.FloatField(
        max_length=10,
        null=True,
        help_text="Себестоимость заказа",
        verbose_name="Общая Себестоимость",
        blank=True,
    )
    organisation_payer = models.ForeignKey(
        Organisation,
        on_delete=models.CASCADE,
        verbose_name="Организация плательщик",
        help_text="Выберите организацию плательщик",
        null=True,
        blank=True,
        default=1
    )
    paid = models.BooleanField(verbose_name="Заказ оплачен", default=False)
    date_complete = models.DateTimeField(
        verbose_name="Дата готовности заказа",
        help_text="Введите дату к которой нужен заказ",
        null=True,
        blank=True,
    )
    comments = models.TextField(verbose_name="Комментарии к заказу", blank=True)
    status = models.ForeignKey(
        StatusOrder, on_delete=models.CASCADE, verbose_name="Статус заказа", default=1
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(  # переименовать в юзера!!!!!
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Заказчик",
        default=1,
    )
    order_arhive = models.FileField(upload_to=f"arhive/{id}", null=True, blank=True)
    order_pdf_file = models.FileField(upload_to=f"orders/", null=True, blank=True)
    pay_link = models.TextField(verbose_name='Ссылка для оплаты', null=True, blank=True)

    def __str__(self):
        return f"Заказ № {self.id}"

    class Meta:
        verbose_name_plural = "Заказы"
        verbose_name = "Заказ"

    def get_absolute_url(self):
        return reverse("orders:add_file_in_order", args=[self.id])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Ордер")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name="Продукт"
    )
    price_per_item = models.FloatField(
        max_length=100, help_text="За 1 шт.", verbose_name="Стоимость шт.", blank=True
    )
    cost_price_per_item = models.FloatField(
        max_length=100,
        help_text="За 1 шт.",
        verbose_name="Себестоимость шт.",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(
        default=1, help_text="Введите количество", verbose_name="Количество"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        verbose_name="Себестоимость Итого",
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Добавлено"
    )  # date created
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Изменено"
    )  # date update

    class Meta:
        verbose_name_plural = "Товары в заказе"
        verbose_name = "Товар в заказе"

    def save(self, *args, **kwargs):
        self.quantity = self.product.quantity
        self.price_per_item = self.product.price
        self.total_price = self.price_per_item  # * self.quantity
        # Cost
        cost_price_per_item = self.product.cost_price
        logger.info(f"cost_price_per_item {cost_price_per_item}")
        self.cost_price_per_item = cost_price_per_item
        self.cost_total_price = self.cost_price_per_item  # * self.quantity

        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.order}-{self.product}"


def product_in_order_post_save(instance, **kwargs):
    order = instance.order
    all_products_in_order = OrderItem.objects.filter(order=order, is_active=True)
    order_total_price = 0
    cost_order_total_price = 0

    for item in all_products_in_order:
        order_total_price += item.total_price
        cost_order_total_price += item.cost_total_price

    instance.order.total_price = order_total_price
    instance.order.cost_total_price = cost_order_total_price
    logger.info(instance.order.total_price)
    logger.info(f"Себестоимость, {cost_order_total_price}")
    instance.order.save(force_update=True)

    # -----------
    """Меняем состояние файла (в заказе)"""


post_save.connect(product_in_order_post_save, sender=OrderItem)


class BankInvoices(models.Model):
    order_id = models.IntegerField(verbose_name='Номер заказа')
    document_id = models.CharField(max_length=40, verbose_name='Номер выставленного документа в банке')
    payment_Status = models.CharField(max_length=40, verbose_name='Статус оплаты', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
