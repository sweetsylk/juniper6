from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse
from recipes.forms import RecipeForm 
from recipes.models import Recipe 

class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    """Update the given recipe"""
    template_name = 'update_recipe.html'
    form_class = RecipeForm
    model = Recipe 
    
    def get_queryset(self):
        """ensure only the author can update their own recipes"""
        return Recipe.objects.filter(author=self.request.user)

    def get_success_url(self):
      
        messages.add_message(self.request, messages.SUCCESS, "your recipe has been done woah!")
        return reverse('dashboard')