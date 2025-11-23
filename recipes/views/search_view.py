from django.shortcuts import render
from django.core.paginator import Paginator
from recipes.models import Recipe

def search_results(request):
    """
    Search recipes by title and display results with pagination.

    - This view searches the Recipe model based on the title field
    - It supports pagination to show 15 recipes per page.

    GET parameters:
    - search (str): the search query string
    - page (int): the page number for pagination (optional)    

    Context:
    - page_obj: paginated recipes for the current page
    - query: the original search query string

    Template:
    - search_results.html
    """

    query = request.GET.get('search', '')
    
    if query:
        recipes = Recipe.objects.filter(title__icontains=query).order_by('-created_at')
    else:
        recipes = Recipe.objects.none()  # empty queryset if no query

    # Pagination
    paginator = Paginator(recipes, 15)  # 15 recipes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Pass paginated recipes and search query to the template 
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'search_results.html', context)
