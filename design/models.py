from django.contrib.auth import get_user_model
from django.db import models

from lids.models import Interest
User = get_user_model()


class DesignOrder(models.Model):
    '''Заказ на создание макета для печати баннера'''
    title = models.CharField(max_length=200,verbose_name='Заголовок')
    # img = models.ForeignKey('ArticleImage', on_delete=models.CASCADE, blank=True, null=True)
    images = models.ImageField(upload_to="image/design", verbose_name="Загрузка файла")

    content = models.TextField(verbose_name='дополнительная информация')
    category = models.ForeignKey(Interest, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(DesignOrder, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    images = models.ImageField(upload_to="image/design", verbose_name="Загрузка файла")

    def __str__(self):
        return f"Comment by {self.author} on {self.article}"