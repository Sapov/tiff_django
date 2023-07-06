# Generated by Django 4.1 on 2023-06-23 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contractor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Поставщик продукции')),
            ],
            options={
                'verbose_name': 'Подрядчикии',
                'verbose_name_plural': 'Подрядчики',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Fields',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fields', models.CharField(max_length=255, verbose_name='Поля вокруг изображения')),
            ],
        ),
        migrations.CreateModel(
            name='FinishWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('work', models.CharField(max_length=255, verbose_name='финишная обработка')),
                ('price_contractor', models.FloatField(blank=True, default=None, help_text='За 1 м. погонный', max_length=100, null=True, verbose_name='Себестоимость работы в руб.')),
                ('price', models.FloatField(help_text='За 1 м. погонный', max_length=100, verbose_name='Стоимость работы в руб.')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default=None, help_text='Введите имя материала для печати', max_length=100, null=True, verbose_name='Материал для печати')),
                ('price_contractor', models.FloatField(blank=True, default=None, help_text='За 1 м2', max_length=100, null=True, verbose_name='Себестоимость печати в руб.')),
                ('price', models.FloatField(help_text='За 1 м2', max_length=100, verbose_name='Стоимость печати в руб.')),
                ('resolution_print', models.IntegerField(blank=True, default=None, help_text='разрешение для печати на материале', null=True, verbose_name='DPI')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы для печати',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TypePrint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_print', models.CharField(max_length=128, verbose_name='Метод печати')),
                ('info_type_print', models.TextField()),
            ],
            options={
                'verbose_name': 'Тип печати',
                'verbose_name_plural': 'Типы печати',
                'ordering': ['type_print'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1, help_text='Введите количество', verbose_name='Количество')),
                ('width', models.FloatField(default=0, help_text='Указывается в см.', verbose_name='Ширина')),
                ('length', models.FloatField(default=0, help_text='Указывается в см.', verbose_name='Длина')),
                ('resolution', models.IntegerField(default=0, help_text='для баннера 72 dpi, для Пленки 150 dpi', verbose_name='Разрешение')),
                ('color_model', models.CharField(choices=[('RGB', 'rgb'), ('CMYK', 'cmyk'), ('GREY', 'Greyscale'), ('LAB', 'lab')], default='CMYK', help_text='Для корректной печати модель должна быть CMYK', max_length=10, verbose_name='Цветовая модель')),
                ('size', models.FloatField(default=0, verbose_name='Размер в Мб')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('images', models.FileField(upload_to='image/%d_%m_%y')),
                ('preview_images', models.FileField(blank=True, default=None, null=True, upload_to='preview')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('Contractor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ЗАКАЗЧИК!!')),
                ('Fields', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.fields', verbose_name='Поля вокруг изображения')),
                ('FinishWork', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='files.finishwork', verbose_name='Финишная обработка')),
                ('material', models.ForeignKey(default='2', on_delete=django.db.models.deletion.CASCADE, to='files.material', verbose_name='Материал')),
            ],
            options={
                'verbose_name': 'Файл',
                'verbose_name_plural': 'Файлы',
            },
        ),
        migrations.AddField(
            model_name='material',
            name='type_print',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='files.typeprint', verbose_name='Тип печати'),
        ),
    ]
