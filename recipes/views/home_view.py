from django.shortcuts import render
#from recipes.views.decorators import login_prohibited
#commented out above and below lines because want to be able to go to home page
#even if logged in

#@login_prohibited
def home(request):
    """Display the application's start/home screen."""
    context = {
    'repeat_times': range(25)
    }

    return render(request, 'home.html', context)

