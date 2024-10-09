# Generated by Django 5.0.7 on 2024-10-06 19:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_alter_order_options_alter_orderitem_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='email address'),
        ),
    ]
