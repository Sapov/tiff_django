from django.db import models

from account.views import Users


class SideGlassСar(models.Model):
    user = models.ForeignKey(Users, on_delete=models.PROTECT, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст на наклейке')
    width = models.IntegerField(verbose_name='Ширина в символах')
    strings = models.IntegerField(verbose_name='Количество строк')
    font = models.CharField(max_length=255, verbose_name='Шрифт')
    size_font = models.IntegerField(verbose_name="Размер шрифта")

