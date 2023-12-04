# Generated by Django 4.1 on 2023-11-22 13:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("account", "0005_deliveryaddress_house"),
    ]

    operations = [
        migrations.AlterField(
            model_name="deliveryaddress",
            name="city",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Город"
            ),
        ),
        migrations.AlterField(
            model_name="deliveryaddress",
            name="house",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Дом"
            ),
        ),
        migrations.AlterField(
            model_name="deliveryaddress",
            name="street",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Улица"
            ),
        ),
    ]