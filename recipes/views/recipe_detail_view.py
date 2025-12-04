from django.shortcuts import render, get_object_or_404
from django.views import View
from recipes.models.recipe import Recipe
from recipes.forms import ReviewForm



class RecipeDetailView(View):
    """Display a recipe"""

    def get(self, request, pk):
        """Handle GET requests by displaying the recipe page"""

        recipe = get_object_or_404(Recipe, pk=pk)

        reviews = recipe.reviews.all()
        review_form = ReviewForm()
        user_review = None

        if request.user.is_authenticated:
            user_review = recipe.reviews.filter(user=request.user).first()
        
        context = {
            "recipe": recipe,
            "reviews": reviews,
            "review_form": review_form,
            "user_review": user_review,
        }


        return render(request, 'display_recipe.html', context)
