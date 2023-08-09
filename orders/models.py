import os
import zipfile
from datetime import date

from django.db import models
from account.models import Organisation
from files.models import Product, StatusProduct
from django.db.models.signals import post_save
from django.urls import reverse

from django.conf import settings
from .utils import Utils, Yadisk


class StatusOrder(models.Model):
    name = models.CharField(max_length=48, verbose_name='Status')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name_plural = 'Статусы'
        verbose_name = 'Статус'


class Order(models.Model):
    total_price = models.FloatField(max_length=10, null=True, help_text='Стоимость заказа',
                                    verbose_name='Общая Стоимость ',
                                    blank=True)
    cost_total_price = models.FloatField(max_length=10, null=True, help_text='Себестоимость заказа',
                                         verbose_name='Общая Себестоимость ',
                                         blank=True)
    organisation_payer = models.ForeignKey(Organisation, on_delete=models.CASCADE,
                                           verbose_name='организация платильщик', default=1)
    paid = models.BooleanField(verbose_name='заказ оплачен', default=False)
    date_complete = models.DateTimeField(verbose_name='Дата готовности заказа',
                                         help_text='Введите дату к которой нужен заказ', null=True, blank=True)
    comments = models.TextField(verbose_name='Comments', blank=True)
    status = models.ForeignKey(StatusOrder, on_delete=models.CASCADE, verbose_name="Статус заказа", default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    Contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ЗАКАЗЧИК!!',
                                   default=1)

    def __str__(self):
        return f'Заказ № {self.id}  {self.organisation_payer}'

    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'

    def get_absolute_url(self):
        return reverse('orders:add_file_in_order', args=[self.id])


def order_post_save(sender, instance, created, **kwargs):
    '''Если статус заказа  (В работе) - меняем все файлы в заказе на статус в работе '''
    status = instance.status
    id_order = instance.id
    if status.id == 2: # Если статус "В работе"
        print('in Work')
        # меняем все файлы в заказе на статус в работе
        all_products_in_order = OrderItem.objects.filter(order=id_order, is_active=True)
        for item in all_products_in_order:
            file = Product.objects.get(id=item.product.id)
            status = StatusProduct.objects.get(id=2)
            file.status_product = status
            file.save()
        # else:
        '''если UNPAID статус заказа оформлен для файлов'''

        lst_files = [str(Product.objects.get(id=item.product.id)) for i in all_products_in_order]
        # архивация заказа
        Utils.set_dir_media()
        Utils.arhvive(lst_files, id_order)  # Архивируемся
        # --------------------------Work in Yandex Disk--------------------------------#
        Yadisk.create_folder()  # Создаем папку на yadisk с датой
        Yadisk.add_yadisk_locate()  # copy files in yadisk
        Yadisk.add_link_from_folder_yadisk()  # Опубликовал папку получил линк


post_save.connect(order_post_save, sender=Order)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Ордер')
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    price_per_item = models.FloatField(max_length=100, help_text='За 1 шт.', verbose_name='Стоимость шт.', blank=True)
    cost_price_per_item = models.FloatField(max_length=100, help_text='За 1 шт.', verbose_name='Себестоимость шт.',
                                            blank=True, null=True)
    quantity = models.IntegerField(default=1, help_text='Введите количество', verbose_name="Количество")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Себестоимость шт.',
                                           blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update

    class Meta:
        verbose_name_plural = 'Товары в заказе'
        verbose_name = 'Товар в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        print(price_per_item)
        self.price_per_item = price_per_item
        self.total_price = self.price_per_item * self.quantity
        # Cost
        cost_price_per_item = self.product.cost_price
        print('cost_price_per_item', cost_price_per_item)
        self.cost_price_per_item = cost_price_per_item
        self.cost_total_price = self.cost_price_per_item * self.quantity

        super(OrderItem, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.order}-{self.product}'


def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = OrderItem.objects.filter(order=order, is_active=True)
    order_total_price = 0
    cost_order_total_price = 0

    for item in all_products_in_order:
        order_total_price += item.total_price
        cost_order_total_price += item.cost_total_price

    instance.order.total_price = order_total_price
    instance.order.cost_total_price = cost_order_total_price
    print(instance.order.total_price)
    print('Себестоимость', cost_order_total_price)
    instance.order.save(force_update=True)

    # -----------
    '''Меняем состояние файла (в заказе)'''
    product = instance.product
    instance.product.in_order = True
    instance.product.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=OrderItem)

# os.remove(f'media/{str(product.images)}')  # Удаление файла
