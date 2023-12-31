# Generated by Django 4.1 on 2023-10-20 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Contractor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='ЗАКАЗЧИК!!'),
        ),
        migrations.AddField(
            model_name='product',
            name='Fields',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='files.fields', verbose_name='Поля вокруг изображения'),
        ),
        migrations.AddField(
            model_name='product',
            name='FinishWork',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='files.finishwork', verbose_name='Финишная обработка'),
        ),
        migrations.AddField(
            model_name='product',
            name='material',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='files.material', verbose_name='Материал'),
        ),
        migrations.AddField(
            model_name='product',
            name='status_product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='files.statusproduct', verbose_name='Статус файла'),
        ),
        migrations.AddField(
            model_name='material',
            name='type_print',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='files.typeprint', verbose_name='Тип печати'),
        ),
    ]
