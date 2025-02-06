from django.shortcuts import render
from .models import Recipe, Category
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404

from .forms import RecipeCreateForm, RecipeUpdateForm

class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'
    paginate_by = 5
    queryset = Recipe.custom.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        context['categories'] = Category.objects.all()
        return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
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


class RecipeCreateView(CreateView):
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
        return super().form_valid(form)


class RecipeUpdateView(UpdateView):
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
        form.save()
        return super().form_valid(form)