from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User


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

    class Meta:
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.title


class Category(models.Model):
    """
    Категория рецепта
    """
    title = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(max_length=255, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=300)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title
