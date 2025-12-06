from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, RecipeReview, User
from recipes.forms import ReviewForm
from recipes.tests.helpers import reverse_with_next

class CreateRecipeReviewViewTestCase(TestCase):
    """Tests for creating or updating recipe reviews."""

    fixtures = [
            'recipes/tests/fixtures/default_user.json',
            'recipes/tests/fixtures/other_users.json',
            'recipes/tests/fixtures/default_recipe.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.get(username='@janedoe')
        self.recipe = Recipe.objects.get(pk=1)

        self.url = reverse('recipe_review', kwargs={'pk': self.recipe.pk})

        self.form_input = {
            'rating' : 5,
            'comment': 'Amazing recipe!',
        }
    
    def test_create_review_url(self):
        self.assertEqual(self.url, f'/recipes/{self.recipe.pk}/review/')

    def test_get_is_not_allowed(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)

    def test_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, data=self.form_input)
        self.assertRedirects(response, redirect_url)

    def test_successful_create_review(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = RecipeReview.objects.count()

        response = self.client.post(self.url, self.form_input, follow=True)

        after_count = RecipeReview.objects.count()
        self.assertEqual(after_count, before_count + 1)

        review = RecipeReview.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Amazing recipe!')

        display_url = reverse('display_recipe', kwargs={'pk': self.recipe.pk})
        self.assertRedirects(response, display_url, target_status_code=200)

        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_successful_update_review(self):
        RecipeReview.objects.create(recipe=self.recipe,user=self.user,rating=3,comment="Okay")

        self.client.login(username=self.user.username, password='Password123')

        response = self.client.post(self.url,{ 'rating': 1, 'comment': 'Terrible now!'}, follow=True)

        display_url = reverse('display_recipe', kwargs={'pk': self.recipe.pk})
        self.assertRedirects(response, display_url)

        self.assertEqual(RecipeReview.objects.filter(recipe=self.recipe,user=self.user).count(),1)

        review = RecipeReview.objects.get(recipe=self.recipe, user=self.user)
        self.assertEqual(review.rating, 1)
        self.assertEqual(review.comment, 'Terrible now!')

        messages_list = list(response.context['messages'])
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_invalid_review_submission(self):
        self.client.login(username=self.user.username, password='Password123')

        before_count = RecipeReview.objects.count()

        invalid_form = {'rating': '', 'comment': 'Missing rating'}

        response = self.client.post(self.url, invalid_form, follow=True)

        after_count = RecipeReview.objects.count()
        self.assertEqual(after_count, before_count)

        messages_list = list(response.context['messages'])
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_user_cannot_edit_other_users_review(self):
        RecipeReview.objects.create(recipe=self.recipe,user=self.other_user,rating=4,comment="Nice")
        
        self.client.login(username=self.user.username, password='Password123')

        response = self.client.post(self.url, self.form_input, follow=True)

        self.assertTrue(RecipeReview.objects.filter(recipe=self.recipe, user=self.other_user, rating=4, comment="Nice").exists())

        self.assertTrue(RecipeReview.objects.filter(recipe=self.recipe, user=self.user, rating=5).exists())