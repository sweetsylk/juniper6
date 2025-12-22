from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from recipes.models import User, Recipe, RecipeReview

"""
GOALS

"what you saved, friends, tags from what you saved"

let you follow tags and hence home feed will show you what is trending in each tag
if a tag you follow is trending it will prompt you to check it out
will show you new posts from people you follow
will show you comments made on recipes you commented on

include have sections- 'because you liked/saved/followed xyz'
    and it will show you posts that other other people who liked that post also liked.
    posts that were liked a lot among fellow like-ees will be shown first
    and same for follows and saves
    by liked i mean 'rated 5 stars', that will go first, then 4 star ratings

should feed be existing and waiting for you? always generated, stored and updated and loaded when
you click on feed, or it should be calulcated when you load the page?
the second option feels like a waste

home feed should exclude recipes you've already liked and saved?

"""

class UserFeedDetailView(LoginRequiredMixin, TemplateView):
    """ 
    Display the logged in user's home feed 
    """
    template_name = "user_feed.html"
    context_object_name = "data"

    def get_queryset(self):
        context = super().get_context_data()
        context['users'] = User.objects.all()
        context['reviews'] = RecipeReview.objects.all()
        context['recipes'] = Recipe.objects.all()

        return context

