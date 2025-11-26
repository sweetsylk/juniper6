from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from recipes.models import User
from recipes.models import Recipe

class UserRecipeListView(LoginRequiredMixin, ListView):
    """
    Return all of the given user's recipes
    """
    
    model = Recipe 
    template_name = "user_recipes.html"
    context_object_name = "recipes"
    paginate_by = 50

    def get_recipes(self):
        
        return Recipe.objects.filter().order_by('-updated_at')
    


