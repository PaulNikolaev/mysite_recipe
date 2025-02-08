from django.test import TestCase
from django.contrib.auth.models import User
from apps.recipe.models import Recipe, Category
from apps.recipe.forms import RecipeCreateForm, RecipeUpdateForm, IngredientForm, StepForm, SearchForm


class RecipeFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(title="Завтраки", description="Вкусные завтраки")

    def test_recipe_create_form_valid(self):
        form_data = {
            'title': 'Новый рецепт',
            'category': self.category.id,
            'description': 'Описание рецепта',
            'cooking_time': 30,
            'servings': 2,
            'status': 'published'
        }
        form = RecipeCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_recipe_update_form_valid(self):
        recipe = Recipe.objects.create(
            title='Обновляемый рецепт',
            author=self.user,
            category=self.category,
            description='Описание',
            cooking_time=20,
            servings=3
        )
        form_data = {
            'title': 'Обновленный рецепт',
            'category': self.category.id,
            'description': 'Обновленное описание',
            'cooking_time': 40,
            'servings': 4,
            'status': 'published',
            'fixed': True
        }
        form = RecipeUpdateForm(data=form_data, instance=recipe)
        self.assertTrue(form.is_valid())


class IngredientFormTest(TestCase):
    def test_ingredient_form_valid(self):
        form_data = {
            'title': 'Мука',
            'amount': 200,
            'quantity': 'грамм'
        }
        form = IngredientForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ingredient_form_invalid(self):
        form_data = {
            'title': '',  # Пустое название
            'amount': -10,  # Отрицательное количество
            'quantity': 'грамм'
        }
        form = IngredientForm(data=form_data)
        self.assertFalse(form.is_valid())


class StepFormTest(TestCase):
    def test_step_form_valid(self):
        form_data = {
            'step_number': 1,
            'description': 'Описание этапа'
        }
        form = StepForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_step_form_invalid(self):
        form_data = {
            'step_number': '',  # Отсутствует номер шага
            'description': ''  # Пустое описание
        }
        form = StepForm(data=form_data)
        self.assertFalse(form.is_valid())


class SearchFormTest(TestCase):
    def test_search_form_valid(self):
        form_data = {'query': 'Пирог'}
        form = SearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_search_form_invalid(self):
        form_data = {'query': ''}  # Пустой запрос
        form = SearchForm(data=form_data)
        self.assertFalse(form.is_valid())
