from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView
from recipes.models import User
from recipes.models import Recipe

class UserRecipesView(LoginRequiredMixin, ListView):

    model = Recipe 
    template_name = "your_recipes.html"
    context_object_name = "recipes"
    paginate_by = 50

    def get_recipes(self):
        #Return all the logged-in user's recipes
        return Recipe.objects.filter(author=self.request.user).order_by('-updated_at')
    


class EditRecipeView():
    pass