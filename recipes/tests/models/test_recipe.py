from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Recipe, User
from recipes.models import RecipeIngredient
from decimal import Decimal

class RecipeModelTestCase(TestCase):
    """This is some tests for the recipe model"""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/default_recipe.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.get(title='Chicken and Rice')

    def test_valid_recipe(self):
        self._assert_recipe_is_valid()

    def test_author_cannot_be_null(self):
        self.recipe.author = None
        self._assert_recipe_is_invalid()

    def test_title_cannot_be_blank(self):
        self.recipe.title = ''
        self._assert_recipe_is_invalid()

    def test_title_can_be_255_characters_long(self):
        self.recipe.title = 'x' * 255
        self._assert_recipe_is_valid()

    def test_title_cannot_be_over_255_characters_long(self):
        self.recipe.title = 'x' * 256
        self._assert_recipe_is_invalid()

    def test_description_cannot_be_blank(self):
        self.recipe.description = ''
        self._assert_recipe_is_invalid()

    def test_prep_time_cannot_be_blank(self):
        self.recipe.prep_time = None
        self._assert_recipe_is_invalid()

    def test_servings_cannot_be_blank(self):
        self.recipe.servings = None
        self._assert_recipe_is_invalid()

    def test_instructions_cannot_be_blank(self):
        self.recipe.instructions = ''
        self._assert_recipe_is_invalid()

    def test_can_add_tags(self):
        self.recipe.tags.add("Lunch", "Protein")
        self.assertIn("Lunch", self.recipe.tags.names())
        self.assertIn("Protein", self.recipe.tags.names())

    def test_string_representation(self):
        self.assertEqual(str(self.recipe), self.recipe.title)

    def _assert_recipe_is_valid(self):
        try:
            self.recipe.full_clean()
        except (ValidationError):
            self.fail('test recipe should be valid but its not')

    def _assert_recipe_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_image_cannot_be_blank(self):
        self.recipe.image = None
        self._assert_recipe_is_invalid()

    def test_prep_time_must_be_at_least_one(self):
        self.recipe.prep_time = 1
        self._assert_recipe_is_valid()
        self.recipe.prep_time = 0
        self._assert_recipe_is_invalid()
        self.recipe.prep_time = -5
        self._assert_recipe_is_invalid()

    def test_servings_must_be_at_least_one(self):
        self.recipe.servings = 1
        self._assert_recipe_is_valid()
        self.recipe.servings = 0
        self._assert_recipe_is_invalid()
        self.recipe.servings = -3
        self._assert_recipe_is_invalid()


class RecipeIngredientModelTestCase(TestCase):
    """Tests for the RecipeIngredient model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/default_recipe.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.get(title='Chicken and Rice')
        self.ingredient = RecipeIngredient(
            recipe=self.recipe,
            name='Salt',
            amount=Decimal('1.00'),
            unit='g',
        )

    def test_valid_ingredient(self):
        self._assert_ingredient_is_valid()

    def test_name_cannot_be_blank(self):
        self.ingredient.name = ''
        self._assert_ingredient_is_invalid()

    def test_amount_must_be_at_least_0_01(self):
        # A value above the minimum should be valid
        self.ingredient.amount = Decimal('0.02')
        self._assert_ingredient_is_valid()

        # Zero should be invalid
        self.ingredient.amount = Decimal('0')
        self._assert_ingredient_is_invalid()

        # Negative should be invalid
        self.ingredient.amount = Decimal('-1')
        self._assert_ingredient_is_invalid()



    def test_unit_must_be_one_of_choices(self):
        self.ingredient.unit = 'kg'
        self._assert_ingredient_is_valid()
        self.ingredient.unit = 'invalid_unit'
        self._assert_ingredient_is_invalid()

    def test_string_representation(self):
        self.assertEqual(str(self.ingredient), "Salt (1.00 g)")


    def _assert_ingredient_is_valid(self):
        try:
            self.ingredient.full_clean()
        except ValidationError:
            self.fail('test ingredient should be valid but it is not')

    def _assert_ingredient_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.ingredient.full_clean()