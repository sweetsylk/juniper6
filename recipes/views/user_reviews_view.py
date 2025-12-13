from django.views.generic import ListView
from recipes.models import RecipeReview

class MyReviewsView(ListView):
    """Display a list of reviews written by the logged-in user"""

    model = RecipeReview
    template_name = 'user_reviews.html'
    context_object_name = 'user_reviews'

    def get_queryset(self):
        """Return the user's reviews ordered from newest to oldest"""
        
        return RecipeReview.objects.filter(user=self.request.user).order_by('-created_at')