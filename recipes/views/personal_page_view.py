from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from recipes.forms import RecipeForm 
from recipes.models import Recipe 

class CreateRecipeView(LoginRequiredMixin, CreateView):
    """ ... """
    template_name = 'personal_page.html'
    form_class = RecipeForm
    model = Recipe 
    
    def form_valid(self, form):
     
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
      
        messages.add_message(self.request, messages.SUCCESS, "your recipe has been done woah!")
        return reverse('dashboard')