from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from recipes.models.recipe import Recipe
from django.http import JsonResponse


class SaveUnsaveRecipeView(LoginRequiredMixin, View):
    """Toggle saving or unsaving a recipe for a logged-in user"""

    def post(self, request, pk):
        """Handle POST requests to save or unsave a recipe"""

        recipe = get_object_or_404(Recipe, pk=pk)

        if request.user in recipe.saved_by.all():
            # unsave
            recipe.saved_by.remove(request.user)
        else:
            # save
            recipe.saved_by.add(request.user)

        # Redirect back to the page the user came from
        next_url = request.POST.get('current_page') or '/explore/'
        return redirect(next_url)