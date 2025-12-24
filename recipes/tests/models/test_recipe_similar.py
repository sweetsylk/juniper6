from django.test import TestCase
from recipes.models import *
from recipes.models.recipe import RecipeSimilar

class RecipeSimilarModelTests(TestCase):
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json',
        'recipes/tests/fixtures/default_recipe.json',
        'recipes/tests/fixtures/other_recipes.json',
        'recipes/tests/fixtures/default_reviews.json',
    ]

    def setUp(self):
        self.userJane = User.objects.get(username='@janedoe')
        self.userPetra = User.objects.get(username='@petrapickles')
        self.rice = Recipe.objects.get(title= "Chicken and Rice")
        self.salad = Recipe.objects.get(title= "Chicken Salad")
        self.cakes = Recipe.objects.get(title= "Fairy Cakes")
        self.cereal = Recipe.objects.get(title= "Cereal")

    def test_positive_review_creates_normalised_similarity(self):
        RecipeSimilar.objects.get(
            recipe_A = self.rice,
            recipe_B = self.salad, 
            similarity_score=1
        )
    
    def test_negetive_reviews_not_included(self):
        with self.assertRaises(RecipeSimilar.DoesNotExist):
            RecipeSimilar.objects.get(recipe_A = self.cereal)
            RecipeSimilar.objects.get(recipe_B = self.cereal)


    def test_uniqueness_enforcer(self):
        before = RecipeSimilar.objects.count()
        RecipeReview.objects.create(
            recipe = self.salad,
            user = self.userJane,
            rating = "4"
        )
        after = RecipeSimilar.objects.count()
        self.assertEqual(before, after)

    def test_activity_ammends_similarity_score(self):
        self.simulate_activity()

        expected_data = [
            {"recipe_A": self.rice.pk, "recipe_B" : self.salad.pk, "similarity_score" : 3},
            {"recipe_A": self.rice.pk, "recipe_B" : self.cakes.pk, "similarity_score" : 1},
            {"recipe_A": self.salad.pk, "recipe_B" : self.cakes.pk, "similarity_score" : 1},
            {"recipe_A": self.rice.pk, "recipe_B" : self.cereal.pk, "similarity_score" : 1},
            {"recipe_A": self.salad.pk, "recipe_B" : self.cereal.pk, "similarity_score" : 1}
        ]

        rows = RecipeSimilar.objects.all()
        actual_data = list(rows.values("recipe_A", "recipe_B", "similarity_score"))
        self.assertCountEqual(actual_data, expected_data)
        

    def test_get_similars(self):
        self.simulate_activity()

        self.assertEqual(
            list(self.rice.get_similar()), [self.salad, self.cakes, self.cereal])
        self.assertEqual(
            list(self.salad.get_similar()), [self.rice, self.cakes, self.cereal])
        self.assertEqual(
            list(self.cakes.get_similar()), [self.rice, self.salad])
        self.assertEqual(
            list(self.cereal.get_similar()), [self.rice, self.salad])


    def simulate_activity(self):
        RecipeReview.objects.create(
            recipe = self.salad,
            user = self.userJane,
            rating = "4"
        )
        RecipeReview.objects.create(
            recipe = self.cakes,
            user = self.userJane,
            rating = "5"
        )
        RecipeReview.objects.create(
            recipe = self.cereal,
            user = self.userJane,
            rating = "2"
        )
        RecipeReview.objects.create(
            recipe = self.rice,
            user = self.userPetra,
            rating = "4"
        )
        RecipeReview.objects.create(
            recipe = self.salad,
            user = self.userPetra,
            rating = "5"
        )