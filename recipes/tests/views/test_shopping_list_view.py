from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from recipes.models.recipe import Recipe, RecipeIngredient

User = get_user_model()


class ShoppingListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="alice",
            email="alice@example.com",
            password="testpass123",
        )

    def test_login_required(self):
        """
        Anonymous users should be redirected to login when accessing shopping list.
        """
        url = reverse("shopping_list", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        # Adjust if your login URL name/path is different
        self.assertIn("/log_in", response.url)

    def test_redirect_if_pk_not_current_user(self):
        """
        If URL pk does not match logged-in user, redirect to current user's list.
        """
        other = User.objects.create_user(
            username="bob",
            email="bob@example.com",
            password="testpass123",
        )

        self.client.login(username="alice", password="testpass123")

        url = reverse("shopping_list", args=[other.pk])
        response = self.client.get(url)

        expected_url = reverse("shopping_list", args=[self.user.pk])
        self.assertRedirects(
            response,
            expected_url,
            status_code=302,
            target_status_code=200,
        )

    def test_aggregates_ingredients_same_name_unit(self):
        """
        Ingredients with same name and unit from multiple saved recipes are summed.
        """
        self.client.login(username="alice", password="testpass123")

        recipe1 = Recipe.objects.create(
            author=self.user,
            title="Recipe 1",
            description="desc",
            prep_time=10,
            servings=1,
            instructions="...",
            image="recipe_images/test1.jpg",
        )
        recipe2 = Recipe.objects.create(
            author=self.user,
            title="Recipe 2",
            description="desc",
            prep_time=5,
            servings=2,
            instructions="...",
            image="recipe_images/test2.jpg",
        )

        recipe1.saved_by.add(self.user)
        recipe2.saved_by.add(self.user)

        RecipeIngredient.objects.create(
            recipe=recipe1,
            name="Yogurt",
            amount=Decimal("10.00"),
            unit="g",
        )
        RecipeIngredient.objects.create(
            recipe=recipe2,
            name="Yogurt",
            amount=Decimal("20.00"),
            unit="g",
        )

        url = reverse("shopping_list", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        ingredients = list(response.context["ingredients"])

        self.assertEqual(len(ingredients), 1)
        item = ingredients[0]
        self.assertEqual(item["name"], "Yogurt")
        self.assertEqual(item["unit"], "g")
        self.assertEqual(item["total_amount"], Decimal("30.00"))

    def test_separates_same_name_different_units(self):
        """
        Same ingredient name but different units should produce separate rows.
        """
        self.client.login(username="alice", password="testpass123")

        recipe1 = Recipe.objects.create(
            author=self.user,
            title="Recipe 1",
            description="desc",
            prep_time=10,
            servings=1,
            instructions="...",
            image="recipe_images/test1.jpg",
        )
        recipe2 = Recipe.objects.create(
            author=self.user,
            title="Recipe 2",
            description="desc",
            prep_time=5,
            servings=2,
            instructions="...",
            image="recipe_images/test2.jpg",
        )

        recipe1.saved_by.add(self.user)
        recipe2.saved_by.add(self.user)

        RecipeIngredient.objects.create(
            recipe=recipe1,
            name="Yogurt",
            amount=Decimal("10.00"),
            unit="g",
        )
        RecipeIngredient.objects.create(
            recipe=recipe2,
            name="Yogurt",
            amount=Decimal("2.00"),
            unit="tbsp",
        )

        url = reverse("shopping_list", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        ingredients = sorted(response.context["ingredients"], key=lambda x: x["unit"])

        self.assertEqual(len(ingredients), 2)

        self.assertEqual(ingredients[0]["name"], "Yogurt")
        self.assertEqual(ingredients[0]["unit"], "g")
        self.assertEqual(ingredients[0]["total_amount"], Decimal("10.00"))

        self.assertEqual(ingredients[1]["name"], "Yogurt")
        self.assertEqual(ingredients[1]["unit"], "tbsp")
        self.assertEqual(ingredients[1]["total_amount"], Decimal("2.00"))

    def test_only_uses_saved_recipes(self):
        """
        Only ingredients from recipes saved by the user should be included.
        """
        self.client.login(username="alice", password="testpass123")

        saved_recipe = Recipe.objects.create(
            author=self.user,
            title="Saved",
            description="desc",
            prep_time=10,
            servings=1,
            instructions="...",
            image="recipe_images/saved.jpg",
        )
        unsaved_recipe = Recipe.objects.create(
            author=self.user,
            title="Not Saved",
            description="desc",
            prep_time=10,
            servings=1,
            instructions="...",
            image="recipe_images/unsaved.jpg",
        )

        saved_recipe.saved_by.add(self.user)

        RecipeIngredient.objects.create(
            recipe=saved_recipe,
            name="Flour",
            amount=Decimal("100.00"),
            unit="g",
        )
        RecipeIngredient.objects.create(
            recipe=unsaved_recipe,
            name="Flour",
            amount=Decimal("999.00"),
            unit="g",
        )

        url = reverse("shopping_list", args=[self.user.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        ingredients = list(response.context["ingredients"])

        self.assertEqual(len(ingredients), 1)
        self.assertEqual(ingredients[0]["name"], "Flour")
        self.assertEqual(ingredients[0]["unit"], "g")
        self.assertEqual(ingredients[0]["total_amount"], Decimal("100.00"))
