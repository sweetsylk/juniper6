from django.shortcuts import render

#@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')