from django.shortcuts import render
#from recipes.views.decorators import login_prohibited
#commented out above and below lines because want to be able to go to home page
#even if logged in

#@login_prohibited

cards_per_page = 25

def home(request):
    """Display the application's home screen, which shows cards_per_page more recent recipes from db."""

    context = {
    'page': 0,
    'recipes': [i for i in range(cards_per_page)], 
    #'recipes' : Recipes.objects.all()[:25], #fetch first 25 recipe objects from from Recipes table. once its been made
    """ LEFT OFF HERE!!!"""
    """ LEFT OFF HERE!!!"""
    """ LEFT OFF HERE!!!"""
    """ LEFT OFF HERE!!!"""

    #for the footer- "showing 1 - 25 of 100":
    'first': 1,
    'last': cards_per_page,
    'total': '[uninitialised]', #initialise with total number of recipes in dbs
    }

    return render(request, 'home.html', context)


def home_show_more(request, page):
    """Display cards_per_page more recipes on home page."""
    
    #page = page of recipes currently on, will have been set by prev calls of home or home_show_more
    page+=1 #page we want to go to
    index = page * cards_per_page #int will = amount of recipes wanna show per page

    context = {
    'page': page,
    'recipe_ids': [i for i in range(cards_per_page)], #!! add !! - initialise w IDs 'index' rows from most recent entry !!
    'first': index + 1, 
    'last': index + cards_per_page,
    'total': '[uninitialised]', #initialise with total number of recipes in dbs
    }

    return render(request, 'home.html', context)


''' 
NOTES 

Making queries in django- https://docs.djangoproject.com/en/4.0/topics/db/queries/
Retrieving objects^^

QuerySet- collection of objects from db. can have 0 or more filters to narrow down query results based on given parameters

"You get a QuerySet by using your model's Manager. Each model has at least one Manager, and it's called objects by default. 
Access it directly via the model class, like so:

    >>> Blog.objects
    <django.db.models.manager.Manager object at ...>
    >>> b = Blog(name='Foo', tagline='Bar')
    >>> b.objects
    Traceback:
        ...
    AttributeError: "Manager isn't accessible via Blog instances."
"
the Managers accessible from model classes only and not instances to enforce separation between “table-level” & “record-level” operations.

    Model.objects.all()
    - descibed all objects in db table. to specify though:

    Model.objects.filter(**kwargs)
    Model.objects.exclude(**kwargs)

    Entry.objects.filter(pub_date__year=2006)



useful sections in making queries section- Chaining filters, Retrieving a single object with get(), Limiting QuerySets, plus more!!

Limiting QuerySets

For example, this returns the first 5 objects (LIMIT 5):
>>> Entry.objects.all()[:5]

This returns the sixth through tenth objects (OFFSET 5 LIMIT 5):
>>> Entry.objects.all()[5:10]

Recipes.objects.all()[:25] gets all fields from first 25 from Recipes model

'''