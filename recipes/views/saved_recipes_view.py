from django.views.generic import ListView
from recipes.models.recipe import Recipe
from django.shortcuts import get_object_or_404
from recipes.models.user import User

class SavedRecipesView(ListView):
    """
    Display a list of recipes that a user has saved
    """

    model = Recipe
    template_name = 'saved_recipes.html'
    context_object_name = 'saved_recipes'

    def get_queryset(self):
        """
        Get the queryset of saved recipes for the specified user
        """

        self.profile_user = get_object_or_404(User, pk=self.kwargs['pk'])
        return self.profile_user.saved_recipes.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['saved_count'] = self.profile_user.saved_recipes.count()
        return context 
