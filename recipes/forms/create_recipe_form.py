from django import forms
from django.forms import inlineformset_factory
from ..models import Recipe, RecipeIngredient

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    instructions = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))

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
            'instructions', 
            'tags', 
            'image'
        ]
       

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
    extra=5,     
    can_delete=True         
)       
