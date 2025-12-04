from django import forms
from recipes.models import RecipeReview

class ReviewForm(forms.ModelForm):
    """
    Form for creating or updating a user's review on a recipe.
    Allows entering a rating (1-5) and an optional text comment.
    """
    class Meta:
        model = RecipeReview
        fields = ['rating','comment']
        
        widgets = {
                'rating': forms.NumberInput(attrs={
                    'min': 1,
                    'max': 5,
                    'class': 'form-control',
                }),
                'comment': forms.Textarea(attrs={
                    'rows': 3,
                    'placeholder': 'Add a comment...',
                    'class': 'form-control',
                }),
        }