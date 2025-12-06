from django.shortcuts import render
from django.core.paginator import Paginator
from taggit.models import Tag
from recipes.models import Recipe


def tag_lookup(request, tag):
    """Display all recipes associated with a tag, with pagination."""

    # Check if tag exists
    try: 
        tag_obj = Tag.objects.get(name=tag)
    except Tag.DoesNotExist:
        return render(request, "tag_lookup.html", {"page_obj": None, "tag": tag})

    # Filter recipes by tag, newest first
    filtered_recipes = (
        Recipe.objects.filter(tags=tag_obj)
        .order_by('-updated_at')
        .distinct()
    )

    paginator = Paginator(filtered_recipes, 50)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "tag_lookup.html", 
                  {"page_obj": page_obj, "tag": tag_obj})