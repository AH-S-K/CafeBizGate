# Generated by Django 4.2.13 on 2024-06-06 16:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_alter_orders_order_id_alter_orders_purchase_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admins',
            name='password',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(8)]),
        ),
        migrations.RemoveField(
            model_name='orders',
            name='products',
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9 ]+$')]),
        ),
        migrations.AlterField(
            model_name='storage',
            name='name',
            field=models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9_]+$')]),
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(through='web.Orders_Product', to='web.product'),
        ),
    ]
