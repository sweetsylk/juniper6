from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from recipes.models import Recipe
from taggit.models import Tag as TagModel


def search_results(request):
    """
    Search recipes by title or author's username or tags and display results with pagination.
    Supports multi word searches and multiple tags separated by hashtags (#)
    Title, author search is done by OR logic, tags are done with AND logic
    Title, author search supports both full phrase match and individual word match
    Tags must match exactly to be included

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

        words = query.split()

        # tags = re.findall(r'#(\S+)', query)
        # normal_terms = re.sub(r'#\S+', '', query).split()

        tags = [word[1:].strip() for word in words if word.startswith('#')]
        normal_terms = [word.strip() for word in words if not word.startswith('#')]

        # print(words)
        print("normal terms: ", normal_terms)
        print("tags: ", tags)

        # recipe filtering (start with all recipes)
        recipes = Recipe.objects.all()

        if normal_terms:
            # full search match
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
        recipes = Recipe.objects.none()  # empty querysetaif no query

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
