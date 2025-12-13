from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from recipes.models import User

class FollowUnfollowView(LoginRequiredMixin, View):
    """
    Toggle follow/unfollow for a given user.
    """

    def post(self, request, pk):
        target_user = get_object_or_404(User, pk=pk)
        current_user = request.user

        if current_user != target_user:
            if current_user in target_user.followers.all():
                # Already following → unfollow
                target_user.followers.remove(current_user)
            else:
                # Not following → follow
                target_user.followers.add(current_user)

        return redirect('display_user_profile', username=target_user.username)
