# Generated by Django 4.1 on 2023-08-03 14:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.FloatField(blank=True, help_text='Стоимость заказа', max_length=10, null=True, verbose_name='Общая Стоимость ')),
                ('paid', models.BooleanField(default=False, verbose_name='заказ оплачен')),
                ('date_complete', models.DateTimeField(blank=True, help_text='Введите дату к которой нужен заказ', null=True, verbose_name='Дата готовности заказа')),
                ('comments', models.TextField(blank=True, verbose_name='Comments')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Contractor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='ЗАКАЗЧИК!!')),
                ('organisation_payer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='account.organisation', verbose_name='организация платильщик')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='StatusOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48, verbose_name='Status')),
                ('is_active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Статус',
                'verbose_name_plural': 'Статусы',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_item', models.FloatField(blank=True, help_text='За 1 шт.', max_length=100, verbose_name='Стоимость шт.')),
                ('quantity', models.IntegerField(default=1, help_text='Введите количество', verbose_name='Количество')),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Изменено')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order', verbose_name='Ордер')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='files.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Товар в заказе',
                'verbose_name_plural': 'Товары в заказе',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='orders.statusorder', verbose_name='Статус заказа'),
        ),
    ]
