from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeFromCategory,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('category/<slug:slug>/', RecipeFromCategory.as_view(), name="recipe_by_category"),
]