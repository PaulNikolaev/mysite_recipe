from django.shortcuts import render
from .models import Recipe
from django.views.generic import ListView

# Create your views here.
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipe/recipe_list.html'
    context_object_name = 'recipes'