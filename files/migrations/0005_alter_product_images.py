# Generated by Django 4.1 on 2023-08-14 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0004_rename_uploadarhive_uploadarh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.FileField(upload_to='image/2023-08-14'),
        ),
    ]
