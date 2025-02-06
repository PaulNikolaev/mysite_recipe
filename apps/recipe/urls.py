from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeFromCategory,
    RecipeCreateView,
    RecipeUpdateView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/<slug:slug>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('category/<slug:slug>/', RecipeFromCategory.as_view(), name="recipe_by_category"),
]