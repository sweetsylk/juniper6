from django.db.models.signals import post_save
from django.dispatch import receiver
from recipes.models import RecipeReview, Recipe


"""
whenever a post request is made for review instance, post_save signal sent
this reciever function checks if rating was positive (>=4), and queries Recipe
model for x other recipes the same user made positive reviews for, and passes
them to Recipe's add_similar() method
"""

@receiver(post_save, sender=RecipeReview)
def handle_new_review(sender, instance, created, **kwargs):
    if created and instance.rating>=4:
        similar_recipes = Recipe.objects.filter(
            reviews__user = instance.user,
            reviews__rating__gte = 4 #rating is >= 4
        ).exclude(
            reviews__recipe = instance.recipe
        )
    instance.recipe.add_similar(similar_recipes)


