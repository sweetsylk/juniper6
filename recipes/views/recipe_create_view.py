from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db import transaction
from recipes.forms import RecipeForm, IngredientFormSet 
from recipes.models import Recipe 

class RecipeCreateView(LoginRequiredMixin, CreateView):
    """Create a new recipe along with its ingredients using a formset."""

    template_name = 'create_recipe.html'
    form_class = RecipeForm
    model = Recipe 
    
    def get_context_data(self, **kwargs):
        """ Include the IngredientFormSet in the context."""

        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['ingredients'] = IngredientFormSet(self.request.POST)
        else:
            context['ingredients'] = IngredientFormSet()

        return context

    def form_valid(self, form):
        """
        Handle saving the recipe AND the ingredient formset.
        Ensures both save together using an atomic transaction.
        """
        context = self.get_context_data()
        ingredients = context['ingredients']
        
      
        with transaction.atomic():
            form.instance.author = self.request.user
            
            if ingredients.is_valid():
                self.object = form.save()
                
                ingredients.instance = self.object
                ingredients.save()
                
                return super().form_valid(form)
            
            # If ingredients are invalid, re-render with errors
            return self.render_to_response(context)

    def get_success_url(self):
        messages.success(self.request, "Recipe created successfully!")
        return reverse('dashboard')