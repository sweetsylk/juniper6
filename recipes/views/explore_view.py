from django.shortcuts import render
from django.core.paginator import Paginator
from recipes.models import Recipe


def explore(request):
    """Display home page, which shows x number of most recent recipes from db."""

    cards_per_page = 100
    
    paginator = Paginator(Recipe.objects.order_by('-created_at'), cards_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "explore.html", {"page_obj": page_obj})
