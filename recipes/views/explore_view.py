
from django.conf import settings

from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from recipes.models import Recipe


def explore(request):
    """Display home page, which shows x number of most recent recipes from db."""

    cards_per_page = 100
    #could add functionality to let user set this value using ?cpp= and cards_per_page = request.GET.get("cpp")
    
    p = Paginator(Recipe.objects.order_by('-created_at'), cards_per_page)
    page_number = request.GET.get("page")
    page_obj = p.get_page(page_number)
    return render(request, "explore.html", {"page_obj": page_obj})


#from django.views.generic import ListView

#class home(ListView):
    
#    model = Recipe 
#    template_name = "home.html"
#    context_object_name = "recipes"
#    paginate_by = 50
