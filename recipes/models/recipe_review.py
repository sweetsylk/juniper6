from django.db import models 
from django.conf import settings 
from recipes.models import Recipe

class RecipeReview(models.Model):
    """
    Stores a user's review for a specific recipe.
    A user can leave exactly one review per recipe.
    """

    # The recipe being reviewed
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    
    # The user who wrote the review
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipe_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevent duplicate reviews by the same user on same recipe
        unique_together = ('recipe','user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipe.title} - {self.rating} stars"