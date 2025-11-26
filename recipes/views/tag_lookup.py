from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from taggit.models import Tag
from recipes.models import Recipe


def tag_lookup(request, tag):
    """Display home page, which shows x number of most recent recipes from db."""

    #check tag exists in db (for when user searches up a tag rather than clicks on existing)
    try: 
        tag_obj = Tag.objects.get(name=tag)

    except Tag.DoesNotExist:
        return render(request, "tag_lookup.html", {"page_obj": None, "tag": tag})

    filtered_recipes = Recipe.objects.filter(tags=tag_obj).order_by('-updated_at').distinct()
    cards_per_page = 50

    p = Paginator(filtered_recipes, cards_per_page)

    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(request, "tag_lookup.html", {"page_obj": page_obj, "tag": tag_obj})