from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm
from recipes.models import User, Recipe, RecipeIngredient

class RecipeCreateViewTestCase(TestCase):
    # this to test the create recipe view

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_recipe')
        self.user = User.objects.get(username='@johndoe')
        
        
        self.form_input = {
            
            'title': 'Philly Cheesestake',
            'description': 'Philly cheese stake meal so yummy',
            'prep_time': 30,
            'servings': 5,
            'instructions': 'IDK just make it bro',
            'tags': 'Meat, American, Sandwich',
            
           
            'ingredients-TOTAL_FORMS': '1', 
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            
           
            'ingredients-0-name': 'Ribeye Steak',
            'ingredients-0-amount': '200',
            'ingredients-0-unit': 'g',
        }

    def test_create_recipe_url(self):
        self.assertEqual(self.url, '/recipes/create/')

    def test_add_ingredient_button(self):
        """
        tests that clicking add ingredient increases the formset total
        and rerenders the page
        """
        self.client.login(username=self.user.username, password='Password123')
        
        payload = self.form_input.copy()
        payload['add_ingredient'] = 'true' 
        
     
        response = self.client.post(self.url, payload)
        

        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'create_recipe.html')
        
        formset = response.context['ingredients']
        total_forms = int(formset.data['ingredients-TOTAL_FORMS'])
        self.assertEqual(total_forms, 2)
        
        
        self.assertEqual(Recipe.objects.count(), 0)

    def test_get_create_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
        
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertFalse(form.is_bound)
        
        self.assertIn('ingredients', response.context)

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
        before_ing_count = RecipeIngredient.objects.count()
        
        response = self.client.post(self.url, self.form_input, follow=True)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        
       
        new_recipe = Recipe.objects.latest('created_at')
        self.assertEqual(new_recipe.title, 'Philly Cheesestake')
        self.assertEqual(new_recipe.author, self.user)
        
       
        self.assertEqual(RecipeIngredient.objects.count(), before_ing_count + 1)
        self.assertEqual(new_recipe.ingredients.first().name, 'Ribeye Steak')

        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)

    def test_unsuccessful_create_recipe(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['title'] = '' # Make the form invalid
        before_count = Recipe.objects.count()
        
        response = self.client.post(self.url, self.form_input)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertTrue(form.errors)