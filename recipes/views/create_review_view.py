from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from recipes.models import Recipe, RecipeReview
from recipes.forms import ReviewForm

class CreateRecipeReviewView(LoginRequiredMixin, View):
    """Handle creating or updating a user's review for a recipe."""

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk = pk)
        form = ReviewForm(request.POST)

        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Updating or create a review (1 review per user)
            review, created = RecipeReview.objects.update_or_create(
                recipe=recipe,
                user=request.user,
                defaults={'rating': rating,'comment': comment}
            )

            if created:
                messages.success(request, "Your review has been added!")
            else:
                messages.success(request, "Your review has been updated!")

        else:
            messages.error(request, "Invalid review submission.")

        return redirect('display_recipe', pk = pk)