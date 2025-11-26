from django.shortcuts import render
from django.views import View


class RecipeDetailView(View):
    """Display a recipe"""

    def get(self, request):
        """Handle GET requests by displaying the recipe page"""

        return render(request, 'display_recipe.html')