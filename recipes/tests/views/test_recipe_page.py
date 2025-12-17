from django.test import TestCase
from django.urls import reverse
from recipes.models import User, Recipe, RecipeIngredient, RecipeInstruction
from datetime import datetime

class RecipePageViewTests(TestCase):
    """
    Tests for the dynamic recipe page (RecipePage view).
    """

    def setUp(self):
        """Create a user and recipe with ingredients."""
        self.user = User.objects.create(username='user', email='user@email.com')

        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Test Recipe",
            description="Test Food",
            prep_time=15,
            servings=3,
            created_at=datetime(2025, 1, 1, 12, 0),
            updated_at=datetime(2025, 1, 1, 12, 0),
        )

        RecipeIngredient.objects.create(
            recipe=self.recipe,
            name="Beef",
            amount=500,
            unit="g"
        )
        RecipeIngredient.objects.create(
            recipe=self.recipe,
            name="Chicken",
            amount=50,
            unit="g"
        )
        RecipeInstruction.objects.create(recipe=self.recipe, step_number=1, text="Step 1")
        RecipeInstruction.objects.create(recipe=self.recipe, step_number=2, text="Step 2")
        RecipeInstruction.objects.create(recipe=self.recipe, step_number=3, text="Step 3")

    def test_recipe_page_loads_successfully(self):
        """
        Test that the recipe page loads successfully with correct content.
        """
        url = reverse('display_recipe', args=[self.recipe.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Recipe")
        self.assertContains(response, "Test Food")

    def test_recipe_page_displays_ingredients(self):
        """
        The recipe page should show ingredient names and amounts.
        """
        url = reverse('display_recipe', args=[self.recipe.id])
        response = self.client.get(url)

        self.assertContains(response, "Beef")
        self.assertContains(response, "500")
        self.assertContains(response, "g")

        self.assertContains(response, "Chicken")
        self.assertContains(response, "50")

    def test_recipe_page_shows_instructions(self):
        """
        Instructions split by lines should be shown as steps.
        """
        url = reverse('display_recipe', args=[self.recipe.id])
        response = self.client.get(url)

        self.assertContains(response, "Step 1")
        self.assertContains(response, "Step 2")
        self.assertContains(response, "Step 3")

    def test_recipe_page_404_for_missing_recipe(self):
        """
        A nonexistent recipe ID should return a 404.
        """
        url = reverse('display_recipe', args=[999999])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
