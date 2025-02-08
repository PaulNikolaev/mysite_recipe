from django.core.cache import cache

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.urls import reverse
from django.utils import timezone
from django.core.files.storage import default_storage

from apps.services.utils import unique_slugify

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.png',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        """
        Сортировка, название таблицы в базе данных
        """
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.user.username, self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Возвращение строки
        """
        return self.user.username

    def get_absolute_url(self):
        """
        Ссылка на профиль
        """
        return reverse('profile_detail', kwargs={'slug': self.slug})

    @property
    def is_online(self):
        cache_key = f'last-seen-{self.user.id}'
        last_seen = cache.get(cache_key)

        if last_seen and timezone.now() - last_seen < timezone.timedelta(seconds=300):
            return True
        return False

    def delete(self, *args, **kwargs):
        # Проверяем, что аватар не является дефолтным
        if self.avatar and self.avatar.name != 'images/avatars/default.png':
            if default_storage.exists(self.avatar.name):
                default_storage.delete(self.avatar.name)

        super().delete(*args, **kwargs)
