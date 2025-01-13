from django.db import models


class Pic(models.Model):
    # width_picturies = models.FloatField(max_length=3, verbose_name='Ширинка картины')
    # length_picturies =
    size_pic = models.CharField(max_length=64, verbose_name='Размер картины')
