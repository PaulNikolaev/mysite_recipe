# Generated by Django 5.1.5 on 2025-02-12 16:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_alter_category_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredient',
            name='amount',
            field=models.FloatField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Количество'),
        ),
    ]
