from django.contrib import admin
from .models import Recipe, Category, Ingredient, Step


class IngredientInline(admin.TabularInline):
    """
    Встроенное отображение ингредиентов на странице рецепта
    """
    model = Ingredient
    extra = 1
    fields = ('title', 'amount', 'quantity')
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'Ингредиенты'


class StepInline(admin.StackedInline):
    """
    Встроенное отображение шагов приготовления на странице рецепта
    """
    model = Step
    extra = 1
    fields = ('step_number', 'description', 'image')
    ordering = ('step_number',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'status', 'create', 'fixed', 'category')
    list_filter = ('status', 'fixed', 'category')
    search_fields = ('title', 'description')
    inlines = [IngredientInline, StepInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title',)
    search_fields = ('title',)
