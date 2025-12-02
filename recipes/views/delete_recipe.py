from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from recipes.models import Recipe
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class DeleteRecipeView(View):
    """Handles deleting a recipe owned by the logged-in user."""
    
    def post(self, request, recipe_id):
        # Fetch the recipe or return 404 if it doesn't exist
        recipe = get_object_or_404(Recipe, id=recipe_id)

        # Check permissions 
        if(recipe.author != request.user):
            messages.error(request,"You are not allowed to delete this recipe.")
            return redirect('profile_view')
        
        # Delete the recipe
        recipe.delete()
        messages.success(request, "Recipe deleted successfully.")
        return redirect('profile_view')