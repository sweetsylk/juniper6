"""
This is the view to help deal with responses and requests within the create_recipe.html page
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db import transaction
from recipes.forms import RecipeForm, IngredientFormSet 
from recipes.models import Recipe, RecipeIngredient

class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_recipe.html'
    form_class = RecipeForm
    model = Recipe 

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        # we are checking if 'ingredients' was already passed (from the post method)
        if 'ingredients' in kwargs:
            data['ingredients'] = kwargs['ingredients']
        else:
            if self.request.POST:
                data['ingredients'] = IngredientFormSet(self.request.POST, prefix='ingredients')
            else:
                data['ingredients'] = IngredientFormSet(queryset=RecipeIngredient.objects.none(), prefix='ingredients')
        
        return data

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        if 'add_ingredient' in request.POST: # so if add ingredient was pressees
            copy = request.POST.copy()
            
            # Use the correct prefix 'ingredients' to find the count
            total_forms_key = 'ingredients-TOTAL_FORMS' 
            current_count = int(copy.get(total_forms_key, 0))
            
            # Increment the form count
            copy[total_forms_key] = current_count + 1
            
            # Initialize the formset with the updated count (copy)
            ingredients = IngredientFormSet(copy, queryset=RecipeIngredient.objects.none(), prefix='ingredients')
            
            form.is_valid() 
            form.errors.clear()
            
            ingredients.is_valid()
            ingredients.errors.clear()
            for subform in ingredients:
                subform.errors.clear()

            # this now returns the form with updated ingredients in its format
            return self.render_to_response(
                self.get_context_data(form=form, ingredients=ingredients)
            )

        # now for the recipe upload overall
        ingredients = IngredientFormSet(request.POST, prefix='ingredients')
        
        if form.is_valid() and ingredients.is_valid():
            return self.form_valid(form, ingredients)
        else:
            return self.form_invalid(form, ingredients)

    def form_valid(self, form, ingredients):
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            ingredients.instance = self.object
            ingredients.save()
        return super().form_valid(form)

    def form_invalid(self, form, ingredients):
        return self.render_to_response(
            self.get_context_data(form=form, ingredients=ingredients))

    def get_success_url(self):
        messages.success(self.request, "Your recipe has been created woah!")
        return reverse('dashboard')