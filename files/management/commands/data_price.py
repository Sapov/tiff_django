# Generated by Django 4.1 on 2023-10-13 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("CUSTOMER_RETAIL", "Клиент"),
                    ("CUSTOMER_AGENCY", "Рекламное агентство"),
                    ("MANAGER", "Менеджер"),
                    ("OPERATOR", "Оператор"),
                    ("FINANCIER", "Бухгалтер"),
                ],
                default="CUSTOMER_RETAIL",
                max_length=24,
            ),
        ),
    ]
