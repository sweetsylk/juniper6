from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Recipe, User

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
        # checking if it can work without foreign key
        self.recipe.author = None
        self._assert_recipe_is_invalid()

    """
    These test for fields
    """

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
        self._assert_recipe_is_invalid() # non is false for this field

    def test_servings_cannot_be_blank(self):
        self.recipe.servings = None
        self._assert_recipe_is_invalid() # non is false for this field

    def test_ingredients_cannot_be_blank(self):
        self.recipe.ingredients = ''
        self._assert_recipe_is_invalid() # non is false for this field

    def test_instructions_cannot_be_blank(self):
        self.recipe.instructions = ''
        self._assert_recipe_is_invalid() # non is false for this field


    def test_image_can_be_blank(self):
        self.recipe.image = None
        self._assert_recipe_is_valid() # non can be true for this field

  
    
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