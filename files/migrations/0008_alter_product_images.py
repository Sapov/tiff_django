# Generated by Django 4.1 on 2023-09-14 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0007_finishwork_is_active_material_is_active_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.FileField(upload_to='image/2023-09-14'),
        ),
    ]