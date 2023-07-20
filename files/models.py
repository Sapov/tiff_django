from django.conf import settings
from django.db import models
from django.urls import reverse

from .tiff_file import check_tiff


class Contractor(models.Model):
    name = models.CharField(max_length=100, verbose_name='Поставщик продукции')

    class Meta:
        verbose_name_plural = 'Подрядчики'
        verbose_name = 'Подрядчикии'
        ordering = ['name']

    def __str__(self):
        return self.name


class TypePrint(models.Model):
    type_print = models.CharField(max_length=128, verbose_name='Метод печати')
    info_type_print = models.TextField()

    class Meta:
        verbose_name_plural = 'Типы печати'
        verbose_name = 'Тип печати'
        ordering = ['type_print']

    def __str__(self):
        return self.type_print


class Material(models.Model):
    name = models.CharField(max_length=100, help_text='Введите имя материала для печати',
                            verbose_name='Материал для печати', blank=True, null=True, default=None)
    type_print = models.ForeignKey(TypePrint, on_delete=models.CASCADE, verbose_name='Тип печати', blank=True,
                                   null=True, default=None)
    price_contractor = models.FloatField(max_length=100, help_text='За 1 м2',
                                         verbose_name='Себестоимость печати в руб.', blank=True, null=True,
                                         default=None)  # стоимость в закупке
    price = models.FloatField(max_length=100, help_text='За 1 м2', verbose_name='Стоимость печати в руб.')
    resolution_print = models.IntegerField(help_text='разрешение для печати на материале', verbose_name='DPI',
                                           blank=True, null=True, default=None)

    def __str__(self):
        return f' {self.name} -     \t- {self.type_print}'

    class Meta:
        verbose_name_plural = 'Материалы для печати'
        verbose_name = 'Материал'
        ordering = ['name']


class Product(models.Model):
    COLOR_MODE = (
        ('RGB', 'rgb'),
        ('CMYK', 'cmyk'),
        ('GREY', 'Greyscale'),
        ('LAB', 'lab')
    )
    Contractor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='ЗАКАЗЧИК!!',
                                   default=1)
    material = models.ForeignKey("Material", on_delete=models.CASCADE, verbose_name='Материал',
                                 default='2')
    quantity = models.IntegerField(default=1, help_text='Введите количество', verbose_name="Количество")
    width = models.FloatField(default=0, verbose_name="Ширина", help_text="Указывается в см.")
    length = models.FloatField(default=0, verbose_name="Длина", help_text="Указывается в см.")
    resolution = models.IntegerField(default=0, verbose_name="Разрешение",
                                     help_text="для баннера 72 dpi, для Пленки 150 dpi")
    color_model = models.CharField(max_length=10, default='CMYK', choices=COLOR_MODE, verbose_name="Цветовая модель",
                                   help_text="Для корректной печати модель должна быть CMYK")
    size = models.FloatField(default=0, verbose_name="Размер в Мб")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)

    images = models.FileField(upload_to='image/%d_%m_%y')
    # preview_images = models.FileField(upload_to='preview', blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено")  # date created
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Изменено")  # date update
    FinishWork = models.ForeignKey('FinishWork', on_delete=models.CASCADE, verbose_name='Финишная обработка', default=1)
    Fields = models.ForeignKey('Fields', on_delete=models.CASCADE, verbose_name='Поля вокруг изображения', default=1)
    in_order = models.BooleanField(verbose_name='Позиция в заказе', default=0, blank=True, null=True)

    # def only_name_file(self):
    #     self.images
    #
    def __str__(self):
        return f'{self.images}'

    def get_absolute_url(self):
        return reverse('files:home')

    class Meta:
        verbose_name_plural = 'Файлы'
        verbose_name = 'Файл'

    def save(self, *args, **kwargs):
        ''' расчет и запись стоимость баннера'''

        self.width, self.length, self.resolution = check_tiff(self.images)  # Читаем размеры из Tiff
        price_per_item = self.material.price
        self.price = round((self.width) / 100 * (self.length) / 100 * self.quantity * price_per_item)
        print(type(self.images))
        # self.preview_images = thumbnail(self.images) # делаем превьюшку
        super(Product, self).save(*args, **kwargs)


class FinishWork(models.Model):
    work = models.CharField(max_length=255, verbose_name='финишная обработка')
    price_contractor = models.FloatField(max_length=100, help_text='За 1 м. погонный',
                                         verbose_name='Себестоимость работы в руб.', blank=True, null=True,
                                         default=None)  # стоимость в закупке
    price = models.FloatField(max_length=100, help_text='За 1 м. погонный', verbose_name='Стоимость работы в руб.')

    def __str__(self):
        return f'{self.work} -- {self.price} руб./1 м.п.'

    class Meta:
        verbose_name_plural = 'Финишная обработка'
        verbose_name = 'Финишная обработка'


class Fields(models.Model):
    fields = models.CharField(max_length=255, verbose_name='Поля вокруг изображения')

    def __str__(self):
        return self.fields

    class Meta:
        verbose_name_plural = 'Поля'
        verbose_name = 'Поле вокруг печати'
