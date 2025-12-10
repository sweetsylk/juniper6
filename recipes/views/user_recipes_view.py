from django.views.generic import ListView
from recipes.models import Recipe

class MyRecipesView(ListView):
    model = Recipe
    template_name = 'user_recipes.html'
    context_object_name = 'user_recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user).order_by('-created_at')