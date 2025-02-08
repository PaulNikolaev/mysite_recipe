from django.test import TestCase
from django.contrib.auth.models import User
from apps.recipe.models import Recipe, Category, Ingredient, Step
from apps.services.utils import unique_slugify


class RecipeModelTest(TestCase):

    def setUp(self):
        """Создаем тестового пользователя и категорию"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.category = Category.objects.create(title="Десерты", description="Разные сладости")

    def test_recipe_creation(self):
        """Тест создания рецепта"""
        recipe = Recipe.objects.create(
            title="Тестовый рецепт",
            description="Описание тестового рецепта",
            cooking_time=30,
            servings=2,
            author=self.user,
            category=self.category
        )
        self.assertEqual(recipe.title, "Тестовый рецепт")
        self.assertEqual(recipe.author.username, "testuser")
        self.assertEqual(recipe.category.title, "Десерты")
        self.assertEqual(recipe.status, "published")

    def test_slug_generation(self):
        """Проверка генерации уникального slug"""
        recipe = Recipe.objects.create(title="Мой тестовый рецепт", author=self.user)
        expected_slug = unique_slugify(recipe, "Мой тестовый рецепт", "")
        self.assertEqual(recipe.slug, expected_slug)

    def test_get_absolute_url(self):
        """Проверка метода get_absolute_url"""
        recipe = Recipe.objects.create(title="Тестовый URL", author=self.user)
        self.assertEqual(recipe.get_absolute_url(), f"/recipes/{recipe.slug}/")


class CategoryModelTest(TestCase):

    def test_category_creation(self):
        """Тест создания категории"""
        category = Category.objects.create(title="Завтраки", description="Вкусные завтраки")
        self.assertEqual(category.title, "Завтраки")
        self.assertEqual(category.description, "Вкусные завтраки")

    def test_category_slug_generation(self):
        """Проверка генерации slug для категории"""
        category = Category.objects.create(title="Мясные блюда")
        expected_slug = unique_slugify(category, "Мясные блюда", "")
        self.assertEqual(category.slug, expected_slug)

    def test_category_get_absolute_url(self):
        """Проверка метода get_absolute_url"""
        category = Category.objects.create(title="Обеды")
        self.assertEqual(category.get_absolute_url(), f"/recipes/category/{category.slug}/")


class IngredientModelTest(TestCase):

    def setUp(self):
        """Создаем пользователя и рецепт"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.recipe = Recipe.objects.create(title="Тестовый рецепт", author=self.user)

    def test_ingredient_creation(self):
        """Тест создания ингредиента"""
        ingredient = Ingredient.objects.create(
            title="Сахар",
            amount=100,
            quantity="грамм",
            recipe=self.recipe
        )
        self.assertEqual(ingredient.title, "Сахар")
        self.assertEqual(ingredient.amount, 100)
        self.assertEqual(ingredient.quantity, "грамм")
        self.assertEqual(ingredient.recipe.title, "Тестовый рецепт")

    def test_ingredient_get_absolute_url(self):
        """Проверка метода get_absolute_url"""
        ingredient = Ingredient.objects.create(title="Сахар", amount=100, recipe=self.recipe)
        self.assertEqual(ingredient.get_absolute_url(), f"/ingredients/edit/{ingredient.pk}/")


class StepModelTest(TestCase):

    def setUp(self):
        """Создаем пользователя и рецепт"""
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.recipe = Recipe.objects.create(title="Тестовый рецепт", author=self.user)

    def test_step_creation(self):
        """Тест создания этапа приготовления"""
        step = Step.objects.create(
            recipe=self.recipe,
            description="Нарежьте лук",
            step_number=1
        )
        self.assertEqual(step.recipe.title, "Тестовый рецепт")
        self.assertEqual(step.description, "Нарежьте лук")
        self.assertEqual(step.step_number, 1)

    def test_step_ordering(self):
        """Проверка сортировки шагов"""
        step1 = Step.objects.create(recipe=self.recipe, description="Добавьте масло", step_number=2)
        step2 = Step.objects.create(recipe=self.recipe, description="Обжарьте лук", step_number=1)
        steps = Step.objects.filter(recipe=self.recipe).order_by('step_number')
        self.assertEqual(steps.first().step_number, 1)  # Проверяем правильный порядок
        self.assertEqual(steps.last().step_number, 2)
