from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from recipes.models import User

class UserProfileView(LoginRequiredMixin, DetailView):

    model = User 
    template_name = "profile_view.html"

    def get_object(self):

        user = self.request.user
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.get_object()
        return context

