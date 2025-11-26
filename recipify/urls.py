"""
URL configuration for recipify project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from recipes import views

urlpatterns = [
    path('admin/', admin.site.urls), 

    path('', views.home, name='home'),
    path('search/', views.search_results, name='search_results'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),

    path('dashboard/', views.dashboard, name='dashboard'), ######
    path('dashboard/drafts/', views.pass_, name='drafts'),
    path('dashboard/history/', views.pass_, name='history'),

    path('settings/profile/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('settings/password/', views.PasswordUpdateView.as_view(), name='update_password'),
    path('settings/filters/', views.pass_, name='update_filters'),
    path('settings/delete/', views.pass_, name='delete_account'),

    path('users/<int:pk>/', views.ProfileDetailView.as_view(), name='display_user_profile'), #view not fully implimented
    path('users/<int:pk>/recipes/', views.UserRecipeListView.as_view(), name='display_user_recipes'), #needs implimentation
    path('users/<int:pk>/likes/', views.pass_, name='display_liked_recipes'),
    path('users/<int:pk>/saves/', views.pass_, name='display_saved_recipes'),
    path('users/<int:pk>/reviews/', views.pass_, name='display_reviewed_recipes'),

    path('recipes/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='display_recipe'), #needs implimentation
    path('recipes/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'), #needs testing
    path('recipes/<int:pk>/delete/', views.pass_, name='delete_recipe'),

    path('tags/<str:tag>/', views.display_tag, name='display_tag'), 
    #filter by tag could use this path with ?= for every added filter maybe
    #tags can have spaces in them, so need to edit Recipe model to use slugs for them
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)