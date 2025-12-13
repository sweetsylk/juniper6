from django.urls import reverse
from django.test import TestCase
from django.contrib import messages
from recipes.models import User, Recipe, RecipeReview

class DeleteReviewTestCase(TestCase):
    """Test for deleting a recipe review"""

    fixtures = [
            'recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/default_recipe.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.recipe = Recipe.objects.get(pk=1)

        self.url = reverse('delete_review', kwargs={'pk': self.recipe.pk})

    def test_redirects_if_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('log_in'))

    def test_user_can_delete_own_review(self):
        RecipeReview.objects.create(recipe=self.recipe, user=self.user,rating=4,comment='Nice')

        self.client.login(username=self.user.username, password='Password123')

        response = self.client.post(self.url, follow=True)

        self.assertFalse(RecipeReview.objects.filter(recipe=self.recipe, user=self.user).exists())

        self.assertRedirects(response, reverse('recipe_reviews', kwargs={'pk': self.recipe.pk}))

        messages_list = list(response.context['messages'])
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_user_cannot_delete_nonexistent_review(self):
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.post(self.url, follow=True)

        messages_list = list(response.context['messages'])
        self.assertEqual(messages_list[0].level, messages.ERROR)