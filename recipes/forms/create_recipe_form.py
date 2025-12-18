from django import forms
from ..models import Recipe, RecipeIngredient, RecipeInstruction
from django.forms import inlineformset_factory, BaseInlineFormSet
from django.core.exceptions import ValidationError
import re
from ..models import Recipe, RecipeIngredient
"""
This is the form for creating a recipe that is on the create_recipe.html page
"""

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    image = forms.ImageField(required=True)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # custom error messages for prep time and servings 
        self.fields['prep_time'].error_messages.update({
        'required': 'Please enter the prep time.',
        'invalid': 'Prep time must be a number.'
        })

        self.fields['servings'].error_messages.update({
            'required': 'Please enter the number of servings.',
            'invalid': 'Servings must be a number.'
        })

    def clean_tags(self):
        tags_data = self.cleaned_data.get('tags')

        if not tags_data:
            raise forms.ValidationError("Please enter at least one tag.")

        # if list then convert to strings
        if isinstance(tags_data, (list, tuple)):
            tags = [str(tag) for tag in tags_data]
        else:
            # if string then split by spaces
            tags = tags_data.strip().split()

        # must start with #, letters/numbers/underscore only
        tag_pattern = re.compile(r'^#[\w]+$')
        for tag in tags:
            if not tag_pattern.match(tag):
                raise forms.ValidationError(
                    f"Invalid tag format: '{tag}'. Tags must start with '#' and contain no spaces."
                )

        return tags  
 

    class Meta:
        model = Recipe
        fields = [
            'title', 
            'description',
            'prep_time', 
            'servings', 
            'tags', 
            'image',
        ]
       
# this is the Ingredient form specifically in which a user can put their ingredient in
class RecipeIngredientForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # custom error messages for prep time and servings 
        self.fields['amount'].error_messages.update({
            'required': 'Please enter an amount.',
            'invalid': 'Amount must be a number.'
        })

    class Meta:
        model = RecipeIngredient
        fields = ['name', 'amount', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Item (e.g banana)'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': '0',
                'step': '0.1' 
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select' 
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        amount = cleaned_data.get('amount')

        if not name or amount is None or amount <= 0:
            raise forms.ValidationError(
                "Each ingredient must have a name and a valid amount."
            )

        return cleaned_data
    
class BaseRecipeIngredientFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        valid_forms = [
            form for form in self.forms
            if form.has_changed() and not form.cleaned_data.get('DELETE', False)
        ]

        if len(valid_forms) < 1:
            raise ValidationError(
                "Please enter at least one ingredient."
            )



IngredientFormSet = inlineformset_factory(
    Recipe,                 
    RecipeIngredient,       
    form=RecipeIngredientForm, 
    formset=BaseRecipeIngredientFormSet,
    extra=1,     
    can_delete=True, 
)       

class RecipeInstructionForm(forms.ModelForm):
    class Meta:
        model = RecipeInstruction
        fields = ['text'] # We can auto-calculate step_number or let user input it
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Explain this step...',
                'rows': 2
            }),
        }

InstructionFormSet = inlineformset_factory(
    Recipe,
    RecipeInstruction,
    form=RecipeInstructionForm,
    extra=1,
    can_delete=True
)