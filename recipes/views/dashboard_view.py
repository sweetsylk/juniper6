from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def dashboard(request):
    """
    Display the dashboard page for the logged-in user.
    """

    return render(request, 'dashboard.html', {'user': request.user})