from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from recipes.forms import RecipeForm 
from recipes.models import Recipe 

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """Allow users to update their own recipes."""

    template_name = 'update_recipe.html'
    form_class = RecipeForm
    model = Recipe 
    
    def get_queryset(self):
        """Only allow the logged-in user to update their own recipes."""
        return Recipe.objects.filter(author=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Recipe updated successfully!")
        return reverse('dashboard')