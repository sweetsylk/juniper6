from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from recipes.models import User, Recipe, RecipeReview
import random

"""
"what you saved, friends, tags from what you saved"

new reviews on posts you reviewed- 
new posts from people you follow- 
new posts from tags you follow- 
"""


class UserFeedDetailView(LoginRequiredMixin, TemplateView):
    """ 
    Display the logged in user's home feed 
    """
    template_name = "user_feed.html"
    context_object_name = "data"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        #find recipes user enjoyed to generate recs from
        recs = set()
        saves = user.saved_recipes.order_by('?')[:10]
        pos_reviewed = Recipe.objects.filter(
            reviews__user = user,
            reviews__rating__gte=4,
        )[:10]

        for recipe in saves: recs.update(recipe.get_similar(10))
        for recipe in pos_reviewed: recs.update(recipe.get_similar(10))
        print(recs)
        
        
        unseen_reviews = list(RecipeReview.objects.filter(
            recipe__in=RecipeReview.objects.filter(user=user).values("recipe"),
        ).exclude(user=user).order_by("-created_at"))[:50]
        
        
        unseen_posts = list(Recipe.objects.filter(
            author__followers=user,
        ).order_by("-created_at"))[:200]

        print(len(recs))
        print(len(unseen_reviews))
        print(len(unseen_posts))
        feed_data = list(recs) + unseen_reviews + unseen_posts
        random.shuffle(feed_data)
        random.shuffle(feed_data)
        print(len(feed_data))

        try: 
            p = Paginator(feed_data, len(feed_data)/3)
            context["col1"] = p.get_page(1)
            context["col2"] = p.get_page(2)
            context["col3"] = p.get_page(3)
            pages = True
        
        except ZeroDivisionError: 
            pages = False
   
        context["user"] = user
        context["feed_data"] = feed_data
        context["pages"] = pages

        return context