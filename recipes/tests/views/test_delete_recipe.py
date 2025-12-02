from django.contrib.messages import get_messages
from django.test import TestCase, Client
from django.urls import reverse
from recipes.models import User, Recipe

class DeleteRecipeViewTestCase(TestCase):

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.other_user = User.objects.create_user(
            username='janedoe',
            email='jane@example.com',
            password='Password123'
        )

        self.recipe = Recipe.objects.create(
            author=self.user,
            title="Delete Test",
            description="Testing deletion",
            prep_time=10, 
            servings=2,
            instructions="Test"
        )

        self.url = reverse('delete_recipe', kwargs={'recipe_id': self.recipe.id})

    def test_delete_recipe_url(self):
        expected_url = f'/dashboard/your_recipes/delete/{self.recipe.id}'
        self.assertEqual(self.url, expected_url)

    def test_post_redirects_if_not_logged_in(self):
        redirect_url = reverse('log_in') + f'?next={self.url}'
        response = self.client.post(self.url)
        self.assertRedirects(response, redirect_url)

    def test_owner_can_delete_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Recipe.objects.count()
        response =self.client.post(self.url,follow=True)
        after_count = Recipe.objects.count()

        self.assertEqual(after_count, before_count-1)
        self.assertRedirects(response, reverse('display_user_profile'))

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level_tag, "success")

    def test_non_owner_cannot_delete_recipe(self):
        self.client.login(username='janedoe', password='Password123')

        before_count = Recipe.objects.count()
        response =self.client.post(self.url,follow=True)
        after_count = Recipe.objects.count()

        self.assertEqual(after_count, before_count)
        self.assertRedirects(response, reverse('display_user_profile'))

        messages_list = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level_tag, "danger")
        self.assertIn("You are not allowed to delete this recipe.", messages_list[0].message)