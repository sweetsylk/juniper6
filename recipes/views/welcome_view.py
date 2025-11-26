from django.shortcuts import render
from recipes.views.decorators import login_prohibited


@login_prohibited
def welcome(request):
    """Display the application's start/home screen."""

    return render(request, 'welcome.html')