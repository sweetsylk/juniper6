from django import forms
from django.forms import inlineformset_factory
from ..models import Recipe, RecipeIngredient, RecipeInstruction
"""
This is the form for creating a recipe that is on the create_recipe.html page
"""

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
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

IngredientFormSet = inlineformset_factory(
    Recipe,                 
    RecipeIngredient,       
    form=RecipeIngredientForm, 
    extra=1,     
    can_delete=True         
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