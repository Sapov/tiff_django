# Generated by Django 4.1 on 2023-08-15 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0005_alter_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.FileField(upload_to='image/2023-08-15'),
        ),
    ]