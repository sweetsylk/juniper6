from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from recipes.models import User, Recipe, RecipeReview

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
        if username: 
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

        # Recipes written by the user
        user_recipes = Recipe.objects.filter(author=user)
        context["user_recipes"] = user_recipes
        context["recipe_count"] = user_recipes.count()
        context["date_joined"] = user.date_joined
        context["saved_count"] = user.saved_recipes.count()

        # All reviews written by the user
        user_reviews = RecipeReview.objects.filter(user=user).select_related("recipe")
        context["user_reviews"] = user_reviews

        # Followers and following users
        context["followers"] = user.followers.all()
        context["following"] = user.following.all()

        # Followers and following count
        context["follower_count"] = user.followers.count()
        context["following_count"] = user.following.count()

        # Flag used by the template to switch between full profile view
        # and recipes-only view (overridden via URL extra_context).
        context.setdefault("show_recipes_only", False)

        return context
