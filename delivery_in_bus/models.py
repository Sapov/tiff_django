from django.contrib.auth import get_user_model
from django.db import models

from orders.models import Order

User = get_user_model()


class OrdersDeliveryBus(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Номер заказа')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Курьер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update
    img_production = models.ImageField(upload_to="img_production/%Y/%m/%d/", verbose_name="Фото продукции в автобусе")
    img_phone = models.ImageField(upload_to="img_phone/%Y/%m/%d/", verbose_name="Фото телефона водителя")
    img_bus = models.ImageField(upload_to="img_bus/%Y/%m/%d/", verbose_name="Фото номера автобуса")
    comments = models.TextField(verbose_name='Комментарии', default='Набрать в 2-00')
