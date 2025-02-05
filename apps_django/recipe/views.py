from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView, DetailView

# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        return context