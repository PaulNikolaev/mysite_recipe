from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.files.storage import default_storage
from apps.recipe.models import Recipe, Step


@receiver(post_delete, sender=Recipe)
def delete_recipe_thumbnail(sender, instance, **kwargs):
    """Удаляем изображение после удаления рецепта"""
    if instance.thumbnail and instance.thumbnail.name != 'images/thumbnails/default.jpg':
        if default_storage.exists(instance.thumbnail.name):
            default_storage.delete(instance.thumbnail.name)


@receiver(post_delete, sender=Step)
def delete_step_image(sender, instance, **kwargs):
    """Удаляем изображение после удаления шага приготовления"""
    if instance.image and instance.image.name != 'images/steps/default.jpg':
        if default_storage.exists(instance.image.name):
            default_storage.delete(instance.image.name)
