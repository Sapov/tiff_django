from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from lids.models import Interest

User = get_user_model()


class OrderDesignStatus(models.TextChoices):
    AWAITING_PAY = 'AWAITING_PAY', 'Ожидает оплаты'
    PAY = 'PAY', 'Оплачен'
    IN_WORK = 'IN_WORK', 'В работе'
    AGREED = 'AGREED', 'УТВЕРЖДЕН'
    CLOSED = 'CLOSED', 'Закрыт'


class Complexity(models.Model):
    complexity_vars = models.CharField(max_length=60, verbose_name='Варианты сложности')
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость разработки')
    teme = models.DateTimeField(verbose_name='Время на разработку')

    def __str__(self):
        return self.complexity_vars

    class Meta:
        verbose_name_plural = 'Варианты сложности макета'

class WorkDesigners(models.Model):
    designer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Дизайнер', null=True, blank=True)
    order_design = models.ForeignKey('OrderDesign', on_delete=models.CASCADE, verbose_name='Заказ на дизайн')
    create_at = models.DateTimeField(auto_now=True, verbose_name='Добавлено'
                                     )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update

    class Meta:
        def __str__(self):
            return self.designer

        verbose_name_plural = 'Заказы по дизайнерам'



class OrderDesign(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название брифа')
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE, verbose_name='Выберите сложность макета',
                                   default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=True, blank=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, verbose_name='Категория макета', default=3)
    width = models.IntegerField(verbose_name='Ширина')
    length = models.IntegerField(verbose_name='Длина')
    description = models.TextField(verbose_name='Тех.задание')
    images = models.ImageField(upload_to='images/designs', verbose_name='Картинка', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    order_status = models.CharField(max_length=100, choices=OrderDesignStatus.choices, verbose_name='Статус Брифа',
                                    default=OrderDesignStatus.AWAITING_PAY)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Брифы'
        verbose_name = 'Бриф'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('designs:design_detail', args=[self.id])  # или kwargs={'pk': self.id}


class Comments(models.Model):
    design = models.ForeignKey(OrderDesign, on_delete=models.CASCADE, related_name='comments', verbose_name='Дизайн'
                               )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name='Текст сообщения')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='comment_images/', blank=True, null=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.design}"

