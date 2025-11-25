from django.test import TestCase
from recipes.forms import RecipeIngredientForm
from recipes.models import RecipeIngredient

class RecipeIngredientFormTestCase(TestCase):
    """
    test specifically for the single Ingredient row form
    """
    def setUp(self):
        self.form_input = {
            'name': 'Chicken Breast',
            'amount': '200',
            'unit': 'g'
        }

    def test_form_contains_required_fields(self):
        form = RecipeIngredientForm()
        self.assertIn('name', form.fields)
        self.assertIn('amount', form.fields)
        self.assertIn('unit', form.fields)
    def test_form_accepts_valid_input(self):
        form = RecipeIngredientForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_name(self):
        self.form_input['name'] = ''
        form = RecipeIngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)

    def test_form_rejects_blank_amount(self):
        self.form_input['amount'] = ''
        form = RecipeIngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_rejects_non_numeric_amount(self):
        self.form_input['amount'] = 'two hundred'
        form = RecipeIngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('amount', form.errors)

    def test_form_accepts_decimal_amount(self):
        # Testing that users can input 1.5 cups
        self.form_input['amount'] = '1.5'
        form = RecipeIngredientForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_uses_correct_widgets(self):
        """Ensure the widgets we set in forms.py (Bootstrap classes) are present"""
        form = RecipeIngredientForm()
        self.assertEqual(form.fields['name'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['amount'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['unit'].widget.attrs['class'], 'form-select')

    def test_unit_must_be_in_choices(self):
        self.form_input['unit'] = 'somali miles' 
        form = RecipeIngredientForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('unit', form.errors)