from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db import transaction # Import transaction for data safety

# Make sure to import the Formset we created in the previous step
from recipes.forms import RecipeForm, IngredientFormSet 
from recipes.models import Recipe 

class CreateRecipeView(LoginRequiredMixin, CreateView):
    template_name = 'create_recipe_page.html'
    form_class = RecipeForm
    model = Recipe 
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['ingredients'] = IngredientFormSet(self.request.POST)
        else:
            data['ingredients'] = IngredientFormSet()
        return data

    def form_valid(self, form):
        """
        This runs when the main RecipeForm is valid. 
        We must now ALSO check if the IngredientFormSet is valid.
        """
        context = self.get_context_data()
        ingredients = context['ingredients']
        
      
        with transaction.atomic():
            form.instance.author = self.request.user
            
            if ingredients.is_valid():
                self.object = form.save()
                
                # link the ingredients to the new recipe and save them
                ingredients.instance = self.object
                ingredients.save()
                
                return super().form_valid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        messages.add_message(self.request, messages.SUCCESS, "Your recipe has been created woah!")
        return reverse('dashboard')