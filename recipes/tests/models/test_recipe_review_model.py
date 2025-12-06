from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import Recipe, RecipeReview, User

class RecipeReviewModelTest(TestCase):

    fixtures = [
            'recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/other_users.json',
            'recipes/tests/fixtures/default_recipe.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.get(pk=1)

    def test_review_creation(self):
        review = RecipeReview.objects.create(
            recipe=self.recipe,
            user=self.user,
            rating=5,
            comment="Greate !"
        )
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Greate !")
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.recipe, self.recipe)

    def test_unique_review_constraint(self):
        RecipeReview.objects.create(
            recipe = self.recipe,
            user = self.user,
            rating = 4,
        )

        duplicate = RecipeReview(
            recipe = self.recipe,
            user = self.user,
            rating = 5,
        )

        with self.assertRaises(ValidationError):
            duplicate.full_clean()
                
    def test_string_representation(self):
        review = RecipeReview.objects.create(
            recipe = self.recipe,
            user = self.user,
            rating = 5,
        )

        expected = f"{self.recipe.title} - 5 stars"
        self.assertEqual(str(review), expected)