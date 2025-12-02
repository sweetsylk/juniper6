from django.shortcuts import render, get_object_or_404
from django.views import View
from recipes.models.recipe import Recipe



class RecipeDetailView(View):
    """Display a recipe"""

    def get(self, request, recipe_id):
        """Handle GET requests by displaying the recipe page"""

        recipe = get_object_or_404(Recipe, id=recipe_id)

        return render(request, 'recipe.html', {"recipe": recipe})
