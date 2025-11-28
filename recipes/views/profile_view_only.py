from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from recipes.models import User, Recipe

class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Displays a user's profile page.
    """
    model = User 
    template_name = "profile_view.html"
    context_object_name = "profile_user"

    def get_object(self):
        """
        Return the User object to display.
        If the URL contains a username, fetch that user.
        Otherwise, return the logged-in user.
        """
        username = self.kwargs.get("username")
        if username is not None: 
            # Show another user's profile 
            return get_object_or_404(User, username=username)
        
        # Show the logged-in user's own profile
        return self.request.user
    
    def get_context_data(self, **kwargs):
        """
        Add recipe information to the template context:
        - All recipes by this user
        - Total recipe count 
        - Date the user joined 
        """
        context = super().get_context_data(**kwargs)
        user = self.get_object()

        user_recipes = Recipe.objects.filter(author=user)

        context["user_recipes"] = user_recipes
        context["recipe_count"] = user_recipes.count()
        context["date_joined"] = user.date_joined
        
        return context

