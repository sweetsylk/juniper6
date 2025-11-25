from django.conf import settings
from django.shortcuts import render
from django.core.paginator import Paginator
from recipes.models import Recipe


def home(request):
    """Display home page, which shows x number of most recent recipes from db."""

    cards_per_page = getattr(settings, "CARDS_PER_PAGE", 50)
    #could add functionality to let user set this value using ?cpp= and cards_per_page = request.GET.get("cpp")

    p = Paginator(Recipe.objects.order_by('-updated_at'), cards_per_page) #costly if db really big no?

    page_number = request.GET.get("page") #if url='', returns none
    page_obj = p.get_page(page_number) #django displays first page if get_page() value = None or invalid

    return render(request, "home.html", {"page_obj": page_obj})


"""
https://docs.djangoproject.com/en/5.2/topics/pagination/

>>> page_obj = p.get_page(page_number)
does: 
- int(page_number)
- returns page obj containing The items on that page (page_obj.object_list)
- returns Pagination info below (among others):

    page_obj.object_list	        The items on this page (QuerySet or list)
    page_obj.number                 Current page number (int)
    page_obj.paginator	            Reference to the parent Paginator object
    page_obj.has_next()	            True if there's a next page
    page_obj.has_previous()	        True if there's a previous page
    page_obj.next_page_number()	    Number of the next page
    page_obj.previous_page_number()	Number of the previous page
    page_obj.start_index()	        Index of first item on this page
    page_obj.end_index()	        Index of last item on this page
    len(page_obj)	                Number of items on this page

"""