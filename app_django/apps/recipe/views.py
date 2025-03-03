import logging
from django.contrib import messages
from django.contrib.postgres.search import TrigramSimilarity
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from .models import Recipe, Category, Ingredient, Step
from .forms import RecipeCreateForm, RecipeUpdateForm, IngredientForm, StepForm, SearchForm
from ..services.mixins import AuthorRequiredMixin

logger = logging.getLogger(__name__)

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 5
    queryset = Recipe.custom.all()

    def get_context_data(self, **kwargs):

        logger.info(f'Загрузка списка рецептов')
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        recipe = self.get_object()
        logger.info(f"Просмотр рецепта: {recipe.title} ({recipe.id})")
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['categories'] = Category.objects.all()
        return context


class RecipeFromCategory(ListView):
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'
    category = None

    def get_queryset(self):
        """
        Возвращает рецепты только для текущей категории.
        """
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Recipe.custom.filter(category=self.category)

    def get_context_data(self, **kwargs):
        """
        Добавляем название категории в контекст.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = f"Категория: {self.category.title}"
        context['categories'] = Category.objects.all()
        return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание рецептов на сайте
    """
    model = Recipe
    template_name = 'recipe/recipe_create.html'
    form_class = RecipeCreateForm
    login_url = 'home'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        logger.info(f"Рецепт создан: {form.instance.title} ({form.instance.id}) пользователем {self.request.user}")
        return response


class RecipeUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления рецепта на сайте
    """
    model = Recipe
    template_name = 'recipe/recipe_update.html'
    context_object_name = 'recipe'
    form_class = RecipeUpdateForm
    login_url = 'home'
    success_message = 'Рецепт был успешно обновлен!'

    def get_context_data(self, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление рецепта: {self.object.title}'
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.updater = self.request.user
        response = super().form_valid(form)
        logger.info(f"Рецепт обновлён: {form.instance.title} ({form.instance.id}) пользователем {self.request.user}")
        return response


class RecipeDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = reverse_lazy('home')
    success_message = 'Рецепт был успешно удалён!'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        recipe = self.get_object()
        logger.warning(f"Рецепт удалён: {recipe.title} ({recipe.id}) пользователем {request.user}")
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, self.success_message)
        return response


class IngredientCreateView(AuthorRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление: Добавление ингредиента в рецепт
    """
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipe/ingredients/add_ingredient.html'

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context


class IngredientUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: Изменение ингредиента в рецепт
    """
    model = Ingredient
    form_class = IngredientForm
    template_name = 'recipe/ingredients/edit_ingredient.html'

    def get_object(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        return get_object_or_404(Ingredient, pk=self.kwargs['pk'], recipe=recipe)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})


class IngredientDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: Удаление ингредиента из рецепта
    """
    model = Ingredient
    template_name = 'recipe/ingredients/delete_ingredient.html'

    def get_object(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        return get_object_or_404(Ingredient, pk=self.kwargs['pk'], recipe=recipe)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})


class StepCreateView(AuthorRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление: Добавление этапа приготовления в рецепт
    """
    model = Step
    form_class = StepForm
    template_name = 'recipe/steps/add_step.html'

    def form_valid(self, form):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        form.instance.recipe = recipe
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context


class StepUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: Изменение этапа приготовления в рецепте
    """
    model = Step
    form_class = StepForm
    template_name = 'recipe/steps/edit_step.html'

    def get_object(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        return get_object_or_404(Step, pk=self.kwargs['pk'], recipe=recipe)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})


class StepDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: Удаление этапа приготовления в рецепте
    """
    model = Step
    template_name = 'recipe/steps/delete_step.html'

    def get_object(self):
        recipe = get_object_or_404(Recipe, slug=self.kwargs['slug'])
        return get_object_or_404(Step, pk=self.kwargs['pk'], recipe=recipe)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs['slug']
        context['categories'] = Category.objects.all()
        return context

    def get_success_url(self):
        return reverse_lazy('recipe_detail', kwargs={'slug': self.kwargs['slug']})


class MyRecipesView(ListView):
    """
    Список рецептов, добавленных текущим пользователем.
    """
    model = Recipe
    template_name = 'recipe/my_recipes.html'
    context_object_name = 'recipes'
    paginate_by = 5

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мои рецепты'
        context['categories'] = Category.objects.all()
        return context


class RecipeSearchView(ListView):
    model = Recipe
    template_name = "recipe/recipe_search.html"
    context_object_name = "recipes"
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get("query")
        if query:
            return Recipe.custom.annotate(
                similarity=TrigramSimilarity("title", query)
            ).filter(similarity__gt=0.1).order_by("-similarity")
        return Recipe.custom.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Результаты поиска"
        context["categories"] = Category.objects.all()
        context["search_form"] = SearchForm(self.request.GET)
        return context



def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    logger.error(f"Ошибка 404: {request.path}")
    return render(request=request, template_name='errors/error_page.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению такая страница была не найдена, или перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    logger.critical("Ошибка 500: внутренняя ошибка сервера")
    return render(request=request, template_name='errors/error_page.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчёт об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    logger.warning(f"Ошибка 403: доступ запрещён для {request.user} к {request.path}")
    return render(request=request, template_name='errors/error_page.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })
