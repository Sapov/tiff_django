# Generated by Django 4.1 on 2023-10-14 00:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("files", "0008_alter_product_images"),
    ]

    operations = [
        migrations.AddField(
            model_name="finishwork",
            name="price_customer_retail",
            field=models.FloatField(
                blank=True,
                help_text="Цена за 1 м. погонный",
                max_length=100,
                null=True,
                verbose_name="Стоимость работы розница в руб.",
            ),
        ),
        migrations.AddField(
            model_name="material",
            name="price_customer_retail",
            field=models.FloatField(
                blank=True,
                help_text="За 1 м2",
                max_length=100,
                null=True,
                verbose_name="Стоимость печати розница в руб.",
            ),
        ),
        migrations.AlterField(
            model_name="material",
            name="price",
            field=models.FloatField(
                help_text="За 1 м2",
                max_length=100,
                verbose_name="Стоимость печати для РА в руб.",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="images",
            field=models.FileField(upload_to="image", verbose_name="Загрузка файла"),
        ),
        migrations.AlterField(
            model_name="product",
            name="material",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                to="files.material",
                verbose_name="Материал",
            ),
        ),
    ]
