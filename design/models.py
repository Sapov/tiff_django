from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from lids.models import Interest
User = get_user_model()


class DesignOrder(models.Model):
    '''Заказ на создание макета для печати баннера'''
    title = models.CharField(max_length=200,verbose_name='Опишите в нескольких словах макет')
    width = models.IntegerField(verbose_name='ширина макета в см')
    length = models.IntegerField(verbose_name='длина макета в см')
    # img = models.ForeignKey('ArticleImage', on_delete=models.CASCADE, blank=True, null=True)
    images = models.ImageField(upload_to="image/design", verbose_name="Загрузите файлы: логотип, брендбук, фото для макета", null=True, blank=True)

    content = models.TextField(verbose_name='дополнительная информация', )
    category = models.ForeignKey(Interest, on_delete=models.CASCADE, verbose_name='Категория брифа', default=3)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False, verbose_name='Работа над макетом завершена')
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("design:detail_design", args=[self.id])

class Comment(models.Model):
    article = models.ForeignKey(DesignOrder, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to="image/design", verbose_name="Загрузка файла")

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"