
from django import forms
from django.test import TestCase
from recipes.forms import RecipeForm
from recipes.models import Recipe

class RecipeFormTestCase(TestCase):
    # this rests the create recipe form

    def setUp(self):
       
        self.form_input = {
            'title': 'Philly Cheesestake',
            'description': 'Philly cheese stake meal so yummy',
            'prep_time': 30,
            'servings': 5,
            'ingredients': 'Ribeye Steak, Melted Cheese, Onions, Bread',
            'instructions': 'IDK just make it bro',
            'tags': 'Meat, American, Sandwich'
        }

    def test_form_contains_required_fields(self):
        form = RecipeForm()
        self.assertIn('title', form.fields)
        self.assertIn('description', form.fields)
        self.assertIn('prep_time', form.fields)
        self.assertIn('servings', form.fields)
        self.assertIn('ingredients', form.fields)
        self.assertIn('instructions', form.fields)
        self.assertIn('tags', form.fields)
        self.assertIn('image', form.fields)

    def test_form_uses_correct_widgets(self):
        form = RecipeForm()
        self.assertIsInstance(form.fields['description'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['ingredients'].widget, forms.Textarea)
        self.assertIsInstance(form.fields['instructions'].widget, forms.Textarea)
        
        # Check widget attributes defined in the form class
        self.assertEqual(form.fields['description'].widget.attrs['rows'], 3)
        self.assertEqual(form.fields['ingredients'].widget.attrs['rows'], 6)
        self.assertEqual(form.fields['instructions'].widget.attrs['rows'], 8)

    def test_form_accepts_valid_input(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_title(self):
        self.form_input['title'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_description(self):
        self.form_input['description'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_ingredients(self):
        self.form_input['ingredients'] = ''
        form = RecipeForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_instructions(self):
        self.form_input['instructions'] = ''
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

    def test_form_accepts_blank_image(self):
        form = RecipeForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_save_handles_model_instance(self):
      
        form = RecipeForm(data=self.form_input)
        if form.is_valid():
            recipe = form.save(commit=False)
            self.assertIsInstance(recipe, Recipe)
            self.assertEqual(recipe.title, 'Philly Cheesestake')
        else:
            self.fail("form aint valid")