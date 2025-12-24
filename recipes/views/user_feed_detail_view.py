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
"""
Look at people you follow- things they liked should be shown to you too?
if 2 users follow the same person

    maybe should be a number then- you guys didn't match again for x number of interactions
    hence remove
    which parties interactions would guarentee this?
    okay, relationship should by asymetrical then
    tbf, i could like a lot of things you like, but you might not like stuff I like
    so if we are matched, add both directions, and then if A doesnt get B
    matched to them again after x interactions, then remove row (A, B, x), but not (B, A, y)
    because B might like stuff A likes, but A doesnt like stuff B likes
    then get_similars would just:
    order sim table by (field[0] = B, -field[2])
    and return all field[1] (if doomscrolling) or first x field[1] if not
    then we give template the list of user objects
    it takes first y of their recent saves, and positive reviews

    IF YOU RATED SOMETHING POORLY shout not be recommended to you!
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

