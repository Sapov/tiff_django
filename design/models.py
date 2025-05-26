from django.db import models
from django.urls import reverse

from lids.models import Interest


class OrderDesign(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE, verbose_name='Категория макета')
    width = models.IntegerField(verbose_name='Ширина')
    length = models.IntegerField(verbose_name='Длина')
    description = models.TextField(verbose_name='Дополнительные сведения')
    images = models.ImageField(upload_to = 'images/design', verbose_name='Картинка')
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")


    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('article_detail', args=[self.slug])
