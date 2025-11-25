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

    path('dashboard/', views.dashboard, name='dashboard'), #users see options to view their profile, posts, saved recipes, comments, ratings etc.
    path('dashboard/your_profile/', views.ViewProfileView.as_view(), name='view_profile'), #users see their account settings and details
    path('dashboard/your_profile/edit', views.EditProfileView.as_view(), name='edit_profile'), #users can update their account settings and details
    path('dashboard/your_profile/edit/password/', views.ChangePasswordView.as_view(), name='change_password'), #seperate pages for more sensitive info like passwords
    path('dashboard/your_recipes/', views.ViewRecipesView.as_view(), name='view_recipes'), 
    path('dashboard/your_recipes/edit/', views.EditRecipeView.as_view(), name='edit_recipe'), 
    path('dashboard/your_favourites/', views.ViewFavouritesView.as_view(), name='view_favourites'), 
    path('dashboard/your_favourites/edit/', views.EditFavouritesView.as_view(), name='edit_favourites'), 

    path('create_recipe/', views.CreateRecipeView.as_view(), name='create_recipe'),

    path('recipe/<int:recipe_id>', views.ViewRecipView.as_view(), name='view_recipe'), #users can view recipes
    path('user/<int:user_id>', views.ViewProfileView.as_view(), name='view_other_profile'), #users can view other users' profiles
    path('tag/<str:tag>', views.tag, name='view_tag'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)