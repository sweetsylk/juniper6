from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from recipes.models import Recipe, RecipeReview

class DeleteReviewView(View):
    """Handle deleting a user's review for a specific recipe"""

    def post(self, request, pk):
        """Delete the logged-in user's review for the given recipe"""

        # Ensure the user is logged in 
        if not request.user.is_authenticated:
            messages.error(request, "You must log in  to delete your review.")
            return redirect('log_in')
        
        recipe = get_object_or_404(Recipe, pk=pk)

        review = RecipeReview.objects.filter(recipe=recipe, user=request.user).first()

        # Delete the review if found
        if review:
            review.delete()
            messages.success(request, "Your review has been deleted successfully!")
        else:
            messages.error(request,"You have no review to delete.")

        return redirect('recipe_reviews', pk=pk)