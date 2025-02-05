from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
]