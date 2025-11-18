from django.shortcuts import render

#from recipes.views.decorators import login_prohibited
#commented out above and below lines because want to be able to go to home page
#even if logged in

#@login_prohibited


"""Need to put pretty much all of this in try/except blocks"""
    #currently if I type some shit like 'http://localhost:8000/200/' it works
    #because not fetching from table, but if i do that once we start fetching, will
    #crash code if not enough recipes in table

"""GLOBALS"""
cards_per_page = 50


def home(request):
    """Display the application's home screen, which shows cards_per_page more recent recipes from db."""

    context = {
    'page': 1,

    'first': 1,
    'last': cards_per_page,

    'total': '[uninitialised]',
    #'total': Recipes.objects.count(),

    'recipes': [i for i in range(cards_per_page)], 
    #'recipes' : Recipes.objects.order_by('-id')[:cards_per_page], 
 
    }

    return render(request, 'home.html', context)


def home_show_more(request, page):
    """Display cards_per_page more recipes on home page."""
    #this code has a bug- will always skip a recipe
    
    #page value passed in = page currently on
    start_idx = page * cards_per_page
    page+=1 #page we want to go to
    end_idx = page * cards_per_page

    context = {
    'page': page,
    'first': start_idx + 1, 
    'last': end_idx,

    'total': '[uninitialised]',
    #'total': Recipes.objects.count(),

    'recipes': [i for i in range(cards_per_page)],
    #'recipes' : Recipes.objects.order_by('-id')[start_idx:end_idx], 
    }

    return render(request, 'home.html', context)




''' 
NOTES 

Making queries in django- https://docs.djangoproject.com/en/5.2/topics/db/queries/
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

>>> Model.objects.last()
- Returns the last object in the QuerySet, or None if empty.

>>> Model.objects.order_by(x).last()

>>> Recipes.objects.all()[:25] 
- gets all fields from first 25 from Recipes model

>>> Model.objects.order_by('id')
- orders the objects with id in ascending order

>>> Model.objects.order_by('-id')
- orders object by '-id', so in descending order

>>> Model.objects.order_by('-id')[:5]
- order with id in descending, then gives first 5
- same as:
    Model.objects.order_by('id')[-5:]
- this one orders in asecnding order, then takes last 5
- but apparently first way is considered cleaner


'''