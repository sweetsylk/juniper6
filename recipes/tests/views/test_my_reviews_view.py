from django.urls import reverse
from django.test import TestCase
from recipes.models import User, Recipe, RecipeReview

class MyReviewsViewTestCase(TestCase):
    """Tests for the user's recipes list view"""

    fixtures = [
            'recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/default_recipe.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        
        self.other_user = User.objects.create_user(
        username='@janedoe',
        email='janedoe@example.com',
        password='Password123'
        )
        
        self.recipe = Recipe.objects.get(pk=1)

        RecipeReview.objects.create(
            recipe=self.recipe,
            user=self.user,
            rating=4,
            comment='Nice'
        )

        RecipeReview.objects.create(
            recipe=self.recipe,
            user=self.other_user,
            rating=2,
            comment='Not great'
        )
        
        self.url = reverse('dashboard_my_reviews')

    def test_view_loads_for_logged_in_user(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_reviews.html')

    def test_only_user_recipes_are_shown(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.get(self.url)
        reviews = response.context['user_reviews']

        self.assertEqual(reviews.count(),1)
        self.assertEqual(reviews[0].user,self.user)