from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm, IngredientFormSet
from recipes.models import User, Recipe, RecipeIngredient, RecipeInstruction
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from django.core.exceptions import NON_FIELD_ERRORS


class RecipeCreateViewTestCase(TestCase):
    """
    Tests the recipe creation view, including GET/POST behaviours,
    redirects for anonymous users, and validation on the main RecipeForm.
    """

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('create_recipe')
        self.user = User.objects.get(username='@johndoe')

        # Create a real in-memory image
        image_io = BytesIO()
        image = Image.new("RGB", (1, 1), color="white")  # 1x1 px
        image.save(image_io, format="PNG")
        image_io.seek(0)

        self.image_file = SimpleUploadedFile(
            "test.png",
            image_io.getvalue(),
            content_type="image/png",
        )

        self.form_input = {
            'title': 'Philly Cheesesteak',
            'description': 'Philly cheese steak meal so yummy',
            'prep_time': 30,
            'servings': 5,
            'tags': '#Meat #American #Sandwich',
            'image': self.image_file,

            # Ingredient Formset data
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': 'Ribeye Steak',
            'ingredients-0-amount': '200',
            'ingredients-0-unit': 'g',

            # Instruction Formset data (NEW)
            'instructions-TOTAL_FORMS': '1', 
            'instructions-INITIAL_FORMS': '0',
            'instructions-MIN_NUM_FORMS': '0',
            'instructions-MAX_NUM_FORMS': '1000',
            'instructions-0-text': 'Cook the steak',
        }

    def test_create_recipe_url(self):
        self.assertEqual(self.url, '/recipes/create/')

    def test_add_ingredient_button(self):
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
        # FIXED: Added definition of before_inst_count
        before_inst_count = RecipeInstruction.objects.count()
        
        response = self.client.post(self.url, self.form_input, follow=True)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        
        new_recipe = Recipe.objects.latest('created_at')
        self.assertEqual(new_recipe.title, 'Philly Cheesesteak')
        self.assertEqual(new_recipe.author, self.user)
         
        self.assertEqual(RecipeIngredient.objects.count(), before_ing_count + 1)
        self.assertEqual(new_recipe.ingredients.first().name, 'Ribeye Steak')

        self.assertEqual(RecipeInstruction.objects.count(), before_inst_count + 1)
        self.assertEqual(new_recipe.instructions.first().text, 'Cook the steak')
        
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

    def test_tags_required(self):
        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'tags': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tags', form.errors)

    def test_invalid_tags_format(self):
        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'tags': 'Meat, American',  # no #, commas
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tags', form.errors)

    def test_valid_tags_format(self):
        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'tags': '#Meat #American',
        })
        self.assertFalse(form.is_valid())  # still missing image
        self.assertNotIn('tags', form.errors)

    def test_image_required(self):
        data = {
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'tags': '#Test',
        }
        form = RecipeForm(data=data)  # no image in files
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

class IngredientFormSetValidationTest(TestCase):
    """
    Tests custom validation logic for the Ingredient inline formset.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='ingredient_user',
            password='Password123'
        )
        # FIXED: Removed 'instructions' string from create call
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test recipe',
            description='Desc',
            prep_time=10,
            servings=1,
        )
        # FIXED: Added mandatory Instruction object
        RecipeInstruction.objects.create(recipe=self.recipe, text='Do stuff')

    def test_requires_at_least_one_ingredient(self):
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': '',
            'ingredients-0-amount': '',
            'ingredients-0-unit': 'g',
        }
        formset = IngredientFormSet(
            data=data,
            instance=self.recipe,
            prefix='ingredients'
        )
        self.assertFalse(formset.is_valid())
        self.assertTrue(
            formset.non_form_errors() or any(f.errors for f in formset.forms)
        )

    def test_invalid_single_ingredient(self):
        data = {
            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',
            'ingredients-0-name': '',
            'ingredients-0-amount': '0',
            'ingredients-0-unit': 'g',
        }
        formset = IngredientFormSet(
            data=data,
            instance=self.recipe,
            prefix='ingredients'
        )
        self.assertFalse(formset.is_valid())