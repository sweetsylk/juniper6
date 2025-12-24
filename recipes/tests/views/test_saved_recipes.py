from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, RecipeIngredient, RecipeInstruction
from recipes.models.user import User

class SavedRecipesViewTests(TestCase):
    """
    Tests for the SavedRecipesView which shows the recipes that a user has saved
    """

    def setUp(self):
        """Create users and recipes, and set up saved recipes."""
        # Create users
        self.user1 = User.objects.create_user(
            username='user1', email='user1@example.com', password='pass1234'
        )
        self.user2 = User.objects.create_user(
            username='user2', email='user2@example.com', password='pass1234'
        )

        # Create recipes
        self.recipe1 = Recipe.objects.create(
            author=self.user1,
            title='Recipe One',
            description='Test recipe one',
            prep_time=10,
            servings=2,
        )
        RecipeInstruction.objects.create(recipe=self.recipe1, text='Do something')

        self.recipe2 = Recipe.objects.create(
            author=self.user2,
            title='Recipe Two',
            description='Test recipe two',
            prep_time=15,
            servings=4,
        )
        RecipeInstruction.objects.create(recipe=self.recipe2, text='Do something else')
        # User1 saves recipe2
        self.recipe2.saved_by.add(self.user1)


    def test_saved_recipes_displays_saved_recipes(self):
        """User only sees the recipes they saved"""
        self.client.login(username='user1', password='pass1234')
        response = self.client.get(reverse('display_saved_recipes', args=[self.user1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Recipe Two')
        self.assertNotContains(response, 'Recipe One')  # User1 didn't saverecipe1

    def test_saved_recipes_no_saved_recipes(self):
        """If user saved no recipes, no recipes should be shown"""
        self.client.login(username='user2', password='pass1234')
        response = self.client.get(reverse('display_saved_recipes', args=[self.user2.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No saved recipes yet')
