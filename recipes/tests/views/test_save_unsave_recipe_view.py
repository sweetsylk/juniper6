from django.test import TestCase
from django.urls import reverse
from recipes.models.user import User
from recipes.models import User, Recipe,RecipeIngredient, RecipeInstruction

class SaveUnsaveRecipeViewTests(TestCase):
    """Tests SaveUnsaveRecipeView which deals with saving and unsaving recipes for a user"""

    def setUp(self):
        """Create a user and recipe for testing"""
        self.user = User.objects.create_user(
            username="user1", email="user1@email.com", password="password123"
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="desc",
            prep_time=10,
            servings=1,
        )
        RecipeInstruction.objects.create(recipe=self.recipe, text="test instructions")

        self.url = reverse("save_unsave_recipe", args=[self.recipe.pk])


    def test_save_recipe(self):
        """
        User can save a recipe
        User is in explore page, should be redirected back to explore page and recipe should be saved
        """
        self.client.login(username="user1", password="password123")

        response = self.client.post(self.url, {"current_page": "/explore/"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/explore/")

        # Check saved
        self.assertIn(self.user, self.recipe.saved_by.all())

    def test_unsave_recipe(self):
        """If a recipe is saved, user can unsave it"""
        self.client.login(username="user1", password="password123")

        # Save once
        self.client.post(self.url, {"current_page": "/explore/"})
        self.assertIn(self.user, self.recipe.saved_by.all())

        # Save again = unsave
        self.client.post(self.url, {"current_page": "/explore/"})
        self.assertNotIn(self.user, self.recipe.saved_by.all())

    def test_redirects_back_to_previous_page(self):
        """Redirect should return user to the page they came from"""
        self.client.login(username="user1", password="password123")

        response = self.client.post(self.url, {"current_page": "/search/?search=pasta+%23cup"})
        self.assertRedirects(response, "/search/?search=pasta+%23cup")


