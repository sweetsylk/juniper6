from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from recipes.forms import UserForm
from recipes.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allow authenticated users to view and update their profile information.
    """

    model = User
    template_name = "update_profile.html"
    form_class = UserForm

    def get_object(self):
        """
        Users can only update their own profile.
        """
        return self.request.user
    
    def form_valid(self, form):
        """
        Save updates and redirect with a success message.
        """
        form.save()
        messages.success(self.request, "Profile updated!")
        return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)