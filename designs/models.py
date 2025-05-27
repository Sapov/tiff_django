from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from lids.models import Interest

User = get_user_model()


class Complexity(models.Model):
    complexity_vars = models.CharField(max_length=60, verbose_name='Варианты сложности')
    description = models.TextField(verbose_name='Описание')
    price = models.PositiveIntegerField(verbose_name='Стоимость разработки')
    teme = models.DateTimeField(verbose_name='Время на разработку')

    def __str__(self):
        return self.complexity_vars

    class Meta:
        verbose_name_plural = 'Варианты сложности макета'


class OrderDesign(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    complexity = models.ForeignKey(Complexity, on_delete=models.CASCADE, verbose_name='Сложность макета')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=True, blank=True)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, verbose_name='Категория макета', default=3)
    width = models.IntegerField(verbose_name='Ширина')
    length = models.IntegerField(verbose_name='Длина')
    description = models.TextField(verbose_name='Дополнительные сведения')
    images = models.ImageField(upload_to='images/designs', verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Брифы'
        verbose_name = 'Бриф'
        ordering = ['title']

    def get_absolute_url(self):
        return reverse('designs:design_detail', args=[self.id])


class Comments(models.Model):
    designs = models.ForeignKey(OrderDesign, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.designs}"
