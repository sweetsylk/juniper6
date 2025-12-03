from django.db import models 
from django.conf import settings 
from recipes.models import Recipe

class RecipeReview(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipe_reviews"
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('recipe','user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipe.title} - {self.rating} stars"