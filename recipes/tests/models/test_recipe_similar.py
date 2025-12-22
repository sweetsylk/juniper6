from django.test import TestCase
from recipes.models import *
from recipes.models.recipe import RecipeSimilar

class RecipeSimilarModelTests(TestCase):

    fixtures = [
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/other_recipes.json',
        'recipes/tests/fixtures/other_reviews.json',
        'recipes/tests/fixtures/default_similar.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@janedoe')
        self.recipe1 = Recipe.objects.get(title = "Chiken and Rice")
        self.recipe2 = Recipe.objects.get(title="Chicken Salad")
        self.review1 = RecipeReview.objects.get(pk=1)
        self.similar1 = RecipeSimilar.objects.get(pk=1)

        """self.recipe1 = Recipe.objects.get(title='Chicken and Rice')
        self.recipe2 = Recipe.objects.get(title='Chicken Salad')
        self.recipe3 = Recipe.objects.get(title='Fairy Cakes')
        self.recipe4 = Recipe.objects.get(title='Cereal')"""

        
    def test_positive_review_creates_similarity():
        new_review = RecipeReview.objects.get(pk=2)


    def test_recipe_order_is_normalized(self):
        new_review = RecipeReview.objects.get(pk=2)
        self.assertEqual(new_review.recipe_A, "")


    """
    check creating positive review makes row
    check reciever creates correct querysets
    check RecipeSimilar is updated correctly when pos rating
    check order normalisaion
    check uniqueness constraint upheld
    check get_similars
    check similarity score increases
    """