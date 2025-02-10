from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth import get_user_model
from django.urls import reverse
import os
from ..services.utils import unique_slugify


User = get_user_model()

class RecipeManager(models.Manager):
    """
    Кастомный менеджер для модели рецептов
    """

    def get_queryset(self):
        """
        Список рецептов (SQL запрос с фильтрацией по статусу опубликованно)
        """
        return super().get_queryset().select_related('author', 'category').filter(status='published')


class Recipe(models.Model):
    """
    Модель рецептов для сайта
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(verbose_name='Название рецепта', max_length=100)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание')
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (в минутах)")
    servings = models.PositiveIntegerField(verbose_name="Количество порций", default=1)
    thumbnail = models.ImageField(
        default='images/thumbnails/default.jpg',
        verbose_name='Изображение рецепта',
        blank=True,
        upload_to='images/thumbnails/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    status = models.CharField(
        choices=STATUS_OPTIONS,
        default='published',
        verbose_name='Статус записи',
        max_length=10
    )
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(
        to=User, verbose_name='Автор',
        on_delete=models.SET_DEFAULT,
        related_name='author_recipe',
        default=1
    )
    updater = models.ForeignKey(
        to=User,
        verbose_name='Обновил',
        on_delete=models.SET_NULL,
        null=True,
        related_name='updater_recipes',
        blank=True
    )
    fixed = models.BooleanField(verbose_name='Прикреплено', default=False)

    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recipes'
    )

    objects = models.Manager()
    custom = RecipeManager()

    class Meta:
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на рецепт
        """
        return reverse('recipe_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Удаляем изображение рецепта при удалении объекта, если оно не дефолтное"""
        if self.thumbnail and self.thumbnail.name != 'images/thumbnails/default.jpg':
            if default_storage.exists(self.thumbnail.name):
                default_storage.delete(self.thumbnail.name)

        super().delete(*args, **kwargs)


class Category(models.Model):
    """
    Категория рецепта
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории',
                                   max_length=300,
                                   blank=True,
                                   null=True,
                                   default='Нет описания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('recipe_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title

    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)


class Ingredient(models.Model):
    """
    Ингредиент для рецепта
    """
    title = models.CharField(verbose_name='Название ингредиента', max_length=100)
    amount = models.PositiveIntegerField(verbose_name="Количество", default=1)
    quantity = models.CharField(max_length=50, verbose_name="Единица измерения", default="грамм")
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='ingredients'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.title} — {self.amount} {self.quantity}"

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на редактирование ингредиента
        """
        return reverse('edit_ingredient', kwargs={'pk': self.pk})


def cooking_step_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f'images/steps/{instance.recipe.slug}/{base}{ext}'


class Step(models.Model):
    """
    Этап приготовления с картинкой
    """
    recipe = models.ForeignKey(
        'Recipe',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='steps'
    )
    description = models.TextField(verbose_name='Описание этапа')
    image = models.ImageField(
        default='images/steps/default.jpg',
        verbose_name='Изображение этапа',
        upload_to=cooking_step_upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif'))]
    )
    step_number = models.PositiveIntegerField(verbose_name='Номер этапа')

    class Meta:
        verbose_name = 'Этап приготовления'
        verbose_name_plural = 'Этапы приготовления'
        ordering = ['step_number']

    def __str__(self):
        return f"Шаг {self.step_number}: {self.description[:30]}..."

    def delete(self, *args, **kwargs):
        """Удаляем изображение шага при удалении объекта, если оно не дефолтное"""
        if self.image and self.image.name != 'images/steps/default.jpg':
            if default_storage.exists(self.image.name):
                default_storage.delete(self.image.name)

        super().delete(*args, **kwargs)
