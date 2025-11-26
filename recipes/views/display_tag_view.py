from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from taggit.models import Tag
from recipes.models import Recipe


def display_tag(request, tag):
    """Display home page, which shows x number of most recent recipes from db."""

    #check tag exists in db (for when user searches up a tag rather than clicks on existing)
    try: 
        tag_obj = Tag.objects.get(name=tag)

    except Tag.DoesNotExist:
        return render(request, "display_tag.html", {"page_obj": None, "tag": tag})

    filtered_recipes = Recipe.objects.filter(tags=tag_obj).order_by('-updated_at').distinct()
    cards_per_page = getattr(settings, "CARDS_PER_PAGE", 50)

    p = Paginator(filtered_recipes, cards_per_page)

    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)

    return render(request, "display_tag.html", {"page_obj": page_obj, "tag": tag_obj})