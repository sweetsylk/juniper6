from django.urls import reverse
from django.test import TestCase
from recipes.models import User, Recipe

class MyRecipeViewTestCase(TestCase):
    """Tests for the user's recipes list view"""

    fixtures = [
            'recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')

        Recipe.objects.create(
        title='My Recipe',
        author=self.user,
        description='Test',
        prep_time=10,
        servings=2,
        instructions='Test instructions'
        )

        Recipe.objects.create(
            title='Other Recipe',
            author=self.other_user,
            description='Test',
            prep_time=15,
            servings=3,
            instructions='Other instructions'
        )
        
        self.url = reverse('dashboard_my_recipes')

    def test_view_loads_for_logged_in_user(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_recipes.html')

    def test_only_user_recipes_are_shown(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)
        recipes = response.context['user_recipes']

        self.assertEqual(recipes.count(),1)
        self.assertEqual(recipes[0].author,self.user)