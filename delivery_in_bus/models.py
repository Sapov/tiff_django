from django.contrib.auth import get_user_model
from django.db import models

from orders.models import Order

User = get_user_model()


class OrdersDeliveryBus(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Номер заказа')
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Курьер")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update
    img_production = models.FileField(upload_to="img_production", verbose_name="Фото упакованной продукции")
    img_phone = models.FileField(upload_to="img_production", verbose_name="Фото телефона водителя")
    img_bus = models.FileField(upload_to="img_production", verbose_name="Фото автобуса")
    comments = models.TextField(verbose_name='Комментарии')
