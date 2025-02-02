# Generated by Django 5.0.6 on 2024-07-03 12:58

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('username', models.CharField(max_length=255, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9_]+$')])),
                ('email', models.EmailField(max_length=255, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('password', models.CharField(max_length=255, unique=True, validators=[django.core.validators.MinLengthValidator(8)])),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('purchase_amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('type', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField()),
                ('purchase_type', models.CharField(choices=[('TA', 'Takeaway'), ('IS', 'Instore')], default='TA', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9آ-ی ]+$')])),
                ('price', models.IntegerField()),
                ('image', models.ImageField(upload_to='images/')),
                ('category', models.CharField(choices=[('CD', 'نوشیدنی سرد'), ('HD', 'نوشیدنی گرم'), ('TI', 'چای و دمنوش'), ('CK', 'کیک')], default='CK', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z0-9آ-ی ]+$')])),
                ('amount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='Orders_Product',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('orders_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.orders')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.product')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='products',
            field=models.ManyToManyField(through='web.Orders_Product', to='web.product'),
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='web.product')),
                ('storage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='web.storage')),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(regex='^[a-zA-Z ]+$')])),
                ('phone_number', models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(code='invalid_phone_number', message='Phone number must be in the format 09xx_xxx_xxxx', regex='^09\\d{9}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='custom_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='username',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='web.users'),
        ),
        migrations.CreateModel(
            name='Users_Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orders_order_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.orders')),
                ('users_username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.users')),
            ],
        ),
    ]
