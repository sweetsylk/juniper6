from django import forms
from ..models import Recipe 

class RecipeForm(forms.ModelForm):
    """
    Form for creating and updating a Recipe. 
    For now its just for user recipes which i have been dealing with
    """

    
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'rows': 6}))
    instructions = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}))

    class Meta:
        model = Recipe
        
        fields = [
            'title', 
            'description', 
            'prep_time', 
            'servings', 
            'ingredients', 
            'instructions', 
            'image'
        ]
        
        labels = {
            'prep_time': 'Prep Time (in minutes)',
            'image': 'Send a picture'
        }