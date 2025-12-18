# recipes/views.py

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Sum


from recipes.models.recipe import Recipe, RecipeIngredient


class ShoppingListView(LoginRequiredMixin, View):
    """
    Aggregate ingredients from all recipes saved by the current user.
    """

    def get(self, request, pk, *args, **kwargs):
        """Get all recipes this user has saved"""

        # Ensure the URL user matches the logged-in user (optional but safer)
        if pk != request.user.pk:
            return redirect('shopping_list', pk=request.user.pk)

        saved_recipes = Recipe.objects.filter(saved_by=request.user)

        ingredients = (
            RecipeIngredient.objects
            .filter(recipe__in=saved_recipes)
            .values('name', 'unit')
            .annotate(total_amount=Sum('amount'))
            .order_by('name')
        )

        context = {
            'ingredients': ingredients,
        }
        return render(request, 'shopping_list.html', context)
