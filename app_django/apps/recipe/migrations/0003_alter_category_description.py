# Generated by Django 5.1.5 on 2025-02-09 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_ingredient_step'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, default='Нет описания', max_length=300, null=True, verbose_name='Описание категории'),
        ),
    ]
