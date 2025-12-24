from django import forms
from django.test import TestCase
# Import the Instruction form and model
from recipes.forms import RecipeInstructionForm 
from recipes.models import RecipeInstruction 

class RecipeInstructionFormTestCase(TestCase):
    """
    Test specifically for the single instruction step form (RecipeInstructionForm).
    This covers the validation and widgets for the 'text' field.
    """
    
    def setUp(self):
        self.form_input = {
            # The field for instruction content is now 'text'
            'text': 'Chop the onions finely and sauté until golden brown.'
        }

    def test_form_contains_required_fields(self):
        form = RecipeInstructionForm()
        self.assertIn('text', form.fields)
        # We don't need to test 'step_number' since it's typically set by the backend/FormSet logic

    def test_form_accepts_valid_input(self):
        """Test that a basic step with text is valid."""
        form = RecipeInstructionForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_text(self):
        """Test that the core instruction text cannot be blank."""
        self.form_input['text'] = ''
        form = RecipeInstructionForm(data=self.form_input)
        self.assertFalse(form.is_valid())
        self.assertIn('text', form.errors)
        self.assertIn('This field is required.', form.errors['text'])

    def test_form_uses_correct_widgets(self):
        """
        Ensure the 'text' field uses a Textarea widget and has the correct
        Bootstrap class and rows attribute set in forms.py.
        """
        form = RecipeInstructionForm()
        
        # Check that it uses a Textarea
        self.assertIsInstance(form.fields['text'].widget, forms.Textarea)
        
        # Check the custom attributes
        self.assertEqual(form.fields['text'].widget.attrs['class'], 'form-control')
        self.assertEqual(form.fields['text'].widget.attrs['rows'], 2)