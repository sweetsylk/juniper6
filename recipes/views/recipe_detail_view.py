from django.shortcuts import render, get_object_or_404
from django.views import View
from recipes.models.recipe import Recipe



class RecipeDetailView(View):
    """Display a single recipe."""

    template_name = "display_recipe.html"

    def get(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        context = {"recipe": recipe}
        return render(request, self.template_name, context)
