# Generated by Django 4.1 on 2023-09-13 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_organisation_phone2_and_more'),
        ('orders', '0002_order_cost_total_price_orderitem_cost_price_per_item_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='organisation_payer',
            field=models.ForeignKey(help_text='Выберите организацию платильщик', on_delete=django.db.models.deletion.CASCADE, to='account.organisation', verbose_name='организация платильщик'),
        ),
    ]