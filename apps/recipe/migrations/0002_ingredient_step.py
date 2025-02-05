# Generated by Django 5.1.5 on 2025-02-05 11:17

import apps.recipe.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Название ингредиента')),
                ('amount', models.PositiveIntegerField(default=1, verbose_name='Количество')),
                ('quantity', models.CharField(default='грамм', max_length=50, verbose_name='Единица измерения')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredients', to='recipe.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='Step',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='Описание этапа')),
                ('image', models.ImageField(blank=True, default='images/steps/default.jpg', null=True, upload_to=apps.recipe.models.cooking_step_upload_to, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))], verbose_name='Изображение этапа')),
                ('step_number', models.PositiveIntegerField(verbose_name='Номер этапа')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='recipe.recipe', verbose_name='Рецепт')),
            ],
            options={
                'verbose_name': 'Этап приготовления',
                'verbose_name_plural': 'Этапы приготовления',
                'ordering': ['step_number'],
            },
        ),
    ]
