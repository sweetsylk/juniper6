from django.shortcuts import render


def show_more(request):
    """Display 25 diff recipes on home page. Could also be used for search results."""
    context = {
    'repeat_times': range(25)
    }

    return render(request, 'home.html', context)

