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

    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),

    path('explore/', views.explore, name='explore'),
    path('search/', views.search_results, name='search_results'),

    path('dashboard/', views.dashboard, name='dashboard'), 
    path('dashboard/drafts/', views.pass_, name='drafts'), 

    path('settings/profile/', views.ProfileUpdateView.as_view(), name='update_profile'),
    path('settings/password/', views.PasswordUpdateView.as_view(), name='update_password'),
    path('settings/filters/', views.pass_, name='update_filters'), 

    path('users/user/', views.ProfileDetailView.as_view(), name='display_user_profile'),
    path('users/<str:username>/', views.ProfileDetailView.as_view(), name='display_user_profile'),
    path('users/<int:pk>/recipes/', views.pass_, name='display_user_recipes'),
    path('users/<int:pk>/reviews/', views.pass_, name='display_reviewed_recipes'), 

    path('recipes/create/', views.RecipeCreateView.as_view(), name='create_recipe'),
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='display_recipe'),
    path('recipes/<int:pk>/update/', views.RecipeUpdateView.as_view(), name='update_recipe'),
    path('recipes/<int:pk>/delete/', views.RecipeDeleteView.as_view(), name='delete_recipe'),
    path('recipes/<int:pk>/save/', views.SaveUnsaveRecipeView.as_view(), name='save_unsave_recipe'),

    path('tags/<str:tag>/', views.tag_lookup, name='display_tag'), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
