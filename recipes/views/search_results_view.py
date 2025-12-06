from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from recipes.models import Recipe
from taggit.models import Tag as TagModel


def search_results(request):
    """
    Search recipes by:
    - title 
    - author username 
    - tags (using #tag format)

    Normal terms use OR logic and support both full-phrase and individual-word matches.
    Tags use AND logic and must match exactly.

    Result are paginated (15 per page) and displayed in search_results.html.
    """

    query = request.GET.get('search', '')
    
    if query:
        words = query.split()

        #Extract tags (#tag) and normal terms 
        tags = [word[1:].strip() for word in words if word.startswith('#')]
        normal_terms = [word.strip() for word in words if not word.startswith('#')]

        recipes = Recipe.objects.all()

        if normal_terms:
            query_filter = Q()
            normal_query = " ".join(normal_terms)
            query_filter |= Q(title__icontains=normal_query) | Q(author__username__icontains=normal_query)

            # individual word match
            for term in normal_terms:
                query_filter |= Q(title__icontains=term) | Q(author__username__icontains=term)

            recipes = recipes.filter(query_filter)

        for tag in tags:
            matching_tags = TagModel.objects.filter(name__iexact=tag)
            if matching_tags.exists():
                recipes = recipes.filter(tags__name__iexact=tag)

            elif not normal_terms:
                recipes = Recipe.objects.none()
                break

        recipes = recipes.distinct().order_by('-created_at')
    else:
        recipes = Recipe.objects.none()

    # Pagination
    paginator = Paginator(recipes, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated recipes and search query to the template 
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'search_results.html', context)
