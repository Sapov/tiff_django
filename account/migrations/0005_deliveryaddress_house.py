# Generated by Django 4.1 on 2023-11-14 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_deliveryaddress_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryaddress',
            name='house',
            field=models.CharField(default=1, max_length=200, verbose_name='Дом'),
            preserve_default=False,
        ),
    ]