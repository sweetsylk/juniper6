from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.shortcuts import redirect
from django.urls import reverse
from recipes.forms import UserForm
from recipes.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Allow authenticated users to view and update their profile information.

    This class-based view displays a user profile editing form and handles
    updates to the authenticated user's profile. Access is restricted to
    logged-in users via `LoginRequiredMixin`.
    """

    model = UserForm
    template_name = "update_profile.html"
    model = User
    template_name = "display_user_profile.html"
    form_class = UserForm

    def get_object(self):
        """
        Retrieve the user object to be edited.

        This ensures that users can only update their own profile, rather
        than any other user's data.

        Returns:
            User: The currently authenticated user instance.
        """
        user = self.request.user
        return user
    
    def form_valid(self, form):
        """
        Save updated profile (including uploaded image) and redirect.
        """
        form.save()
        messages.success(self.request, "Profile updated!")
        return redirect(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
