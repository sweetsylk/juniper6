
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm
from recipes.models import User, Recipe

class CreateRecipeViewTestCase(TestCase):
    # this to test the create recipe view

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_recipe')
        self.user = User.objects.get(username='@johndoe')
        
        # a valid input
        self.form_input = {
            'title': 'Philly Cheesestake',
            'description': 'Philly cheese stake meal so yummy',
            'prep_time': 30,
            'servings': 5,
            'ingredients': 'Ribeye Steak, Melted Cheese, Onions, Bread',
            'instructions': 'IDK just make it bro',
            'tags': 'Meat, American, Sandwich'
        }

    def test_create_recipe_url(self):
        self.assertEqual(self.url, '/create_recipe/')

    def test_get_create_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe_page.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertFalse(form.is_bound)

    def test_get_create_recipe_redirects_when_not_logged_in(self):
        redirect_url = reverse('log_in') + f'?next={self.url}'
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_create_recipe_redirects_when_not_logged_in(self):
        redirect_url = reverse('log_in') + f'?next={self.url}'
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_create_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Recipe.objects.count()
        
        response = self.client.post(self.url, self.form_input, follow=True)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        
        new_recipe = Recipe.objects.latest('created_at')
        self.assertEqual(new_recipe.title, 'Philly Cheesestake')
        self.assertEqual(new_recipe.author, self.user) # making sure the author was assigned automativally
        
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(str(messages_list[0]), "your recipe has been done woah!")
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_unsuccessful_create_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['title'] = ''
        before_count = Recipe.objects.count()
        
        response = self.client.post(self.url, self.form_input)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe_page.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertTrue(form.errors)