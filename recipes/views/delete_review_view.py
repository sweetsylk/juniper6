from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Avg
from django.contrib import messages
from recipes.models import Recipe, RecipeReview
from recipes.forms import ReviewForm

class DeleteReviewView(View):

    def post(self, request, pk):
        if not request.user.is_authenticated:
            messages.error(request, "You must log in  to delete your review.")
            return redirect('log_in')
        
        recipe = get_object_or_404(Recipe, pk=pk)

        review = RecipeReview.objects.filter(recipe=recipe, user=request.user).first()

        if review:
            review.delete()
            messages.success(request, "Your review has been deleted successfully!")
        else:
            messages.error(request,"You have no review to delete.")

        return redirect('recipe_reviews', pk=pk)