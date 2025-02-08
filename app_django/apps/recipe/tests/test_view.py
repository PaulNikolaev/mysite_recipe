from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe, Category

User = get_user_model()

class RecipeViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(title='Test Category', slug='test-category')
        self.recipe = Recipe.objects.create(
            title='Test Recipe', category=self.category, author=self.user, slug='test-recipe'
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse('recipe_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_list.html')

    def test_recipe_detail_view(self):
        response = self.client.get(reverse('recipe_detail', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_detail.html')

    def test_recipe_create_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipe_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_create.html')

    def test_recipe_update_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipe_update', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_update.html')

    def test_recipe_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('recipe_delete', kwargs={'slug': self.recipe.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_delete.html')
