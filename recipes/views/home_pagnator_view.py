from django.shortcuts import render
from django.core.paginator import Paginator
from models import Recipes



"""
Need to put pretty much all of this in try/except blocks
currently if I type some shit like 'http://localhost:8000/200/' it works
because not fetching from table, but if i do that once we start fetching, will
crash code if not enough recipes in table
"""
    


def home_paginator(request):
    """Display home page, which shows cards_per_page more recent recipes from db."""
    cards_per_page = 50

    p = Paginator(Recipes.objects.order_by('-id'), cards_per_page) #costly if db really big no?

    page_number = request.GET.get("page") #passed in through ?page= in html page
    page_obj = p.get_page(page_number) 
    
    context = {
        "page_obj": page_obj
    }

    return render(request, "home.html", context)


"""

>>> page_obj = p.get_page(page_number)
does: 
- int(page_number)
- returns page obj containing The items on that page (page_obj.object_list)
- returns Pagination info: .has_next(), .has_previous(), .next_page_number(), .previous_page_number(), etc.


p.get_page(page_number) returns many things, including:

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