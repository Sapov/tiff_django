from django.db import models
from account.models import Organisation
from files.models import Product


class Order(models.Model):
    organisation_payer = models.ForeignKey(Organisation, on_delete=models.CASCADE,
                                           verbose_name='организация платильщик')
    paid = models.BooleanField(verbose_name='заказ оплачен')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id}-{self.organisation_payer}'



    class Meta:
        verbose_name_plural = 'Заказы'
        verbose_name = 'Заказ'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Ордер')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    price = models.FloatField(max_length=100, help_text='За 1 м2', verbose_name='Стоимость печати в руб.')
    quantity = models.IntegerField(default=1, help_text='Введите количество', verbose_name="Количество")\
