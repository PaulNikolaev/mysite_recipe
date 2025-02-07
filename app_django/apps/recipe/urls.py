from django.urls import path
from .views import (
    RecipeListView,
    RecipeDetailView,
    RecipeFromCategory,
    RecipeCreateView,
    RecipeUpdateView,
    RecipeDeleteView,
    IngredientCreateView,
    IngredientUpdateView,
    IngredientDeleteView,
    StepCreateView,
    StepUpdateView,
    StepDeleteView,
    MyRecipesView,
    RecipeSearchView,
)

urlpatterns = [
    path('', RecipeListView.as_view(), name='home'),
    path('recipe/create/', RecipeCreateView.as_view(), name='recipe_create'),
    path('my_recipes/', MyRecipesView.as_view(), name='my_recipes'),
    path('recipe/<slug:slug>/', RecipeDetailView.as_view(), name='recipe_detail'),
    path('recipe/<slug:slug>/update/', RecipeUpdateView.as_view(), name='recipe_update'),
    path('recipe/<slug:slug>/delete/', RecipeDeleteView.as_view(), name='recipe_delete'),
    path('recipe/<slug:slug>/add_ingredient/', IngredientCreateView.as_view(), name='add_ingredient'),
    path('recipe/<slug:slug>/ingredient/<int:pk>/edit/', IngredientUpdateView.as_view(), name='edit_ingredient'),
    path('recipe/<slug:slug>/ingredient/<int:pk>/delete/', IngredientDeleteView.as_view(), name='delete_ingredient'),

    path('recipe/<slug:slug>/add_step/', StepCreateView.as_view(), name='add_step'),
    path('recipe/<slug:slug>/step/<int:pk>/edit/', StepUpdateView.as_view(), name='edit_step'),
    path('recipe/<slug:slug>/step/<int:pk>/delete/', StepDeleteView.as_view(), name='delete_step'),

    path('search/', RecipeSearchView.as_view(), name='recipe_search'),

    path('category/<slug:slug>/', RecipeFromCategory.as_view(), name='recipe_by_category'),

]
