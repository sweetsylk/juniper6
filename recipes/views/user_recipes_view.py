from django.views.generic import ListView
from recipes.models import Recipe

class MyRecipesView(ListView):
    """Display a list of recipes created by the logged-in user"""

    model = Recipe
    template_name = 'user_recipes.html'
    context_object_name = 'user_recipes'

    def get_queryset(self):
        """Return the user's recipes ordered from newest to oldest"""

        return Recipe.objects.filter(author=self.request.user).order_by('-created_at')