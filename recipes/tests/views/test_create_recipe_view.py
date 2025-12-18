from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from recipes.forms import RecipeForm
from recipes.models import User, Recipe, RecipeIngredient
from recipes.forms import IngredientFormSet
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
            'instructions': 'IDK just make it bro',
            'tags': '#Meat #American #Sandwich',
            'image': self.image_file,

            'ingredients-TOTAL_FORMS': '1',
            'ingredients-INITIAL_FORMS': '0',
            'ingredients-MIN_NUM_FORMS': '0',
            'ingredients-MAX_NUM_FORMS': '1000',

            'ingredients-0-name': 'Ribeye Steak',
            'ingredients-0-amount': '200',
            'ingredients-0-unit': 'g',
        }



    def test_create_recipe_url(self):
        """
        Ensure that the named URL for the create recipe view resolves to the expected path.
        """

        self.assertEqual(self.url, '/recipes/create/')

    def test_add_ingredient_button(self):
        """
        When the add-ingredient button is pressed, the view should
        increase the formset TOTAL_FORMS and re-render the template
        without creating a Recipe instance.
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
        """
        Authenticated GET to the create view should return the template,an unbound RecipeForm, and an ingredients formset in the context.
        """

        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_recipe.html')
        
        form = response.context['form']
        self.assertTrue(isinstance(form, RecipeForm))
        self.assertFalse(form.is_bound)
        
        self.assertIn('ingredients', response.context)

    def test_get_create_recipe_redirects_when_not_logged_in(self):
        """
        Anonymous GET requests should be redirected to the login page with the next parameter set to the create recipe URL
        """

        redirect_url = reverse('log_in') + f'?next={self.url}'
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_post_create_recipe_redirects_when_not_logged_in(self):
        """
        Anonymous POST requests should also be redirected to the login page,
        preventing recipe creation for non-authenticated users.
        """

        redirect_url = reverse('log_in') + f'?next={self.url}'
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_successful_create_recipe(self):
        """
        A valid POST from an authenticated user should create a Recipe and associated RecipeIngredient, then redirect to the dashboard with a success message
        """

        self.client.login(username=self.user.username, password='Password123')
        before_count = Recipe.objects.count()
        before_ing_count = RecipeIngredient.objects.count()
        
        response = self.client.post(self.url, self.form_input, follow=True)
        
        after_count = Recipe.objects.count()
        self.assertEqual(after_count, before_count + 1)
        
       
        new_recipe = Recipe.objects.latest('created_at')
        self.assertEqual(new_recipe.title, 'Philly Cheesesteak')
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
        """
        An invalid POST (e.g. missing title) should not create a Recipe and
        should re-render the create template with form errors.
        """

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
        """
        RecipeForm should be invalid when tags are omitted, and
        should report a validation error on the tags field.
        """

        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'instructions': 'Do stuff',
            'tags': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tags', form.errors)

    def test_invalid_tags_format(self):
        """
        RecipeForm should be invalid when tags do not follow the
        '#tag' format enforced by clean_tags (e.g. commas, missing '#').
        """

        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'instructions': 'Do stuff',
            'tags': 'Meat, American',  # no #, commas
        })
        self.assertFalse(form.is_valid())
        self.assertIn('tags', form.errors)

    def test_valid_tags_format(self):
        """
        RecipeForm should accept correctly formatted tags (e.g. '#Meat #American') and not add errors to the tags field, although the form as a whole is still invalid due to the missing image.
        """

        form = RecipeForm(data={
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'instructions': 'Do stuff',
            'tags': '#Meat #American',
        })
        self.assertFalse(form.is_valid())  # still missing image
        self.assertNotIn('tags', form.errors)

    def test_image_required(self):
        """
        RecipeForm should be invalid when no image is provided, and
        should report a validation error on the image field.
        """

        data = {
            'title': 'Test',
            'description': 'Desc',
            'prep_time': 10,
            'servings': 2,
            'instructions': 'Do stuff',
            'tags': '#Test',
        }
        form = RecipeForm(data=data)  # no image in files
        self.assertFalse(form.is_valid())
        self.assertIn('image', form.errors)

class IngredientFormSetValidationTest(TestCase):
    """
    Tests the custom validation logic for the Ingredient inline formset,including the requirement for at least one ingredient and per-ingredient rules.
    """

    def setUp(self):
        """
        Create a user and a simple Recipe instance to attach the IngredientFormSet to.
        """
        self.user = User.objects.create_user(
            username='ingredient_user',
            password='Password123'
        )
        self.recipe = Recipe.objects.create(
            author=self.user,
            title='Test recipe',
            description='Desc',
            prep_time=10,
            servings=1,
            instructions='Do stuff',
        )

    def test_requires_at_least_one_ingredient(self):
        """
        The IngredientFormSet should be invalid when no ingredient has any meaningful data, enforcing the rule that at least one ingredient must be provided.
        """
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
        # At least some error exists (either form or formset level)
        self.assertTrue(
            formset.non_form_errors() or any(f.errors for f in formset.forms)
        )

    def test_invalid_single_ingredient(self):
        """
        The IngredientFormSet should be invalid when a single ingredient has an empty name or non-positive amount, as enforced by the RecipeIngredientForm.clean method.
        """
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