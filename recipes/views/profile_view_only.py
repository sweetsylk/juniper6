from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from recipes.models import User, Recipe

class UserProfileView(LoginRequiredMixin, DetailView):

    model = User 
    template_name = "profile_view.html"

    def get_object(self):
        user = self.request.user
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context["profile_user"] = user
        context["recipe_count"] = Recipe.objects.filter(author=user).count()
        context["user_recipes"] = Recipe.objects.filter(author=user)
        context["date_joined"] = user.date_joined
        
        return context

