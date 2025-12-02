from django.shortcuts import render, get_object_or_404
from django.views import View
from recipes.models.recipe import Recipe



class RecipeDetailView(View):
    """Display a recipe"""

    def get(self, request, pk):
        """Handle GET requests by displaying the recipe page"""

        recipe = get_object_or_404(Recipe, pk=pk)

        return render(request, 'display_recipe.html', {"recipe": recipe})
