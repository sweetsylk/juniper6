from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Avg
from django.contrib import messages
from django.db.models.signals import post_save
from django.dispatch import receiver
from recipes.models import Recipe, RecipeReview
from recipes.forms import ReviewForm

class RecipeReviewsView(View):
    """Display and handle reviews for a specific recipe"""
    
    def get(self, request, pk):
        """Display the recipe review page"""

        recipe = get_object_or_404(Recipe, pk=pk)
        reviews = RecipeReview.objects.filter(recipe=recipe)
        
        # Get the current user's review (if logged-in)
        user_review = None 
        if request.user.is_authenticated:
            user_review = RecipeReview.objects.filter(recipe=recipe, user=request.user).first()

        form = ReviewForm()

        avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']

        context = {
            'recipe': recipe,
            'reviews': reviews,
            'user_review': user_review,
            'review_form': form,
            'avg_rating': avg_rating,
            'review_count': reviews.count(),
        }

        return render(request, "recipe_reviews.html", context)
    
    def post(self, request, pk):
        """Handle creating or updating a review"""

        if not request.user.is_authenticated:
            messages.error(request, "You must log in to leave a review.")
            return redirect('log_in')
        
        recipe = get_object_or_404(Recipe, pk=pk)
        form = ReviewForm(request.POST)
        
        if form.is_valid():
            rating = form.cleaned_data['rating']
            comment = form.cleaned_data['comment']

            # Create a new review or update the existing one 
            review, created = RecipeReview.objects.update_or_create(
                recipe = recipe,
                user = request.user,
                defaults={'rating': rating, 'comment': comment}
            )

            if created:
                messages.success(request, "Your review has been added!")
            else:
                messages.success(request, "Your review has been updated!")
        else:
            messages.error(request, "Invalid review submission.")
        
        return redirect('recipe_reviews', pk=pk)
