from django.shortcuts import render
from django.views import View


class RecipePage(View):
    """Display the recipe page"""

    def get(self, request):
        """Handle GET requests by displaying the recipe page"""

        return render(request, 'recipe.html')