from django.contrib.auth.mixins import LoginRequiredMixin
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

class UserFeedDetailView(LoginRequiredMixin):
    """ 
    Display the logged in user's home feed 
    """
    model = User 
    template_name = "display_user_profile.html"
    context_object_name = "users"

    


