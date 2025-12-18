from django import forms
from django.test import TestCase
from recipes.forms import RecipeForm
from recipes.models import Recipe, User

class RecipeFormTestCase(TestCase):
    # This tests the create recipe form

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/default_recipe.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'title': 'Philly Cheesestake',
            'description': 'Philly cheese stake meal so yummy',
            'prep_time': 30,
            'servings': 5,
            'tags': '#Meat #American #Sandwich'
        }
      

    def test_form_contains_required_fields(self):
        form = RecipeForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('prep_time', form.fields)
        self.assertIn('servings', form.fields)
        self.assertIn('tags', form.fields)
        self.assertIn('image', form.fields)
       
    def test_form_uses_correct_widgets(self):
        form = RecipeForm()
        self.assertIsInstance(form.fields['description'].widget, forms.Textarea)
        
        # Check that your forms.py sets these attributes correctly
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)


    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_prep_time(self):
        self.form_input['prep_time'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_non_integer_prep_time(self):
        self.form_input['prep_time'] = 'thirty'
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_servings(self):
        self.form_input['servings'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_non_integer_servings(self):
        self.form_input['servings'] = 'five'
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

