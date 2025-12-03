from django import forms
from recipes.models import RecipeReview

class ReviewForm(forms.ModelForm):
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