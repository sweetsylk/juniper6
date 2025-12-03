from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from recipes.models import User, Recipe

class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    Displays a user's profile page.
    """
    model = User 
    template_name = "display_user_profile.html"
    context_object_name = "profile_user"

    def get_object(self):
        """
        Return the User object to display.
        If the URL contains a username, fetch that user.
        Otherwise, return the logged-in user.
        """
        username = self.kwargs.get("username")
        if username is not None: 
            return get_object_or_404(User, username=username)
        
        return self.request.user
    
    
    def get_context_data(self, **kwargs):
        """
        Add additional profile data:
        - All recipes by this user
        - Total recipe count 
        - Date the user joined 
        """
        context = super().get_context_data(**kwargs)
        user = context["profile_user"]

        user_recipes = Recipe.objects.filter(author=user)

        context["user_recipes"] = user_recipes
        context["recipe_count"] = user_recipes.count()
        context["date_joined"] = user.date_joined
        
        return context
