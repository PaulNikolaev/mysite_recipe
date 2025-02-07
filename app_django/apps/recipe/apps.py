from django.apps import AppConfig


class RecipeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.recipe'
    verbose_name = 'Рецепт'
    verbose_name_plural = 'Рецепты'
