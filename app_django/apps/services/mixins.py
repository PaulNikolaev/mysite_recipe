from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from apps.recipe.models import Recipe


class AuthorRequiredMixin(AccessMixin):
    """
    Миксин для проверки, что пользователь является автором рецепта или администратором.
    """

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Для выполнения этого действия необходимо войти в систему.')
            return redirect('login')

        # Получаем объект рецепта через slug из URL
        recipe = get_object_or_404(Recipe, slug=self.kwargs.get('slug'))

        # Проверяем, является ли пользователь автором или администратором
        if not (request.user == recipe.author or request.user.is_staff):
            messages.info(request, 'Действие доступно только автору рецепта или администратору!')
            return redirect('home')

        return super().dispatch(request, *args, **kwargs)