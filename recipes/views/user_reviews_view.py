from django.views.generic import ListView
from recipes.models import RecipeReview

class MyReviewsView(ListView):
    model = RecipeReview
    template_name = 'user_reviews.html'
    context_object_name = 'user_reviews'

    def get_queryset(self):
        return RecipeReview.objects.filter(user=self.request.user).order_by('-created_at')