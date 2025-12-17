from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.db import transaction
from recipes.forms import RecipeForm, IngredientFormSet, InstructionFormSet
from recipes.models import Recipe, RecipeIngredient, RecipeInstruction

class RecipeCreateView(LoginRequiredMixin, CreateView):
    template_name = 'create_recipe.html'
    form_class = RecipeForm
    model = Recipe 

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        
        if 'ingredients' in kwargs:
            data['ingredients'] = kwargs['ingredients']
        else:
            if self.request.POST:
                data['ingredients'] = IngredientFormSet(self.request.POST, prefix='ingredients')
            else:
                data['ingredients'] = IngredientFormSet(queryset=RecipeIngredient.objects.none(), prefix='ingredients')
        
        if 'instructions' in kwargs:
            data['instructions'] = kwargs['instructions']
        else:
            if self.request.POST:
                data['instructions'] = InstructionFormSet(self.request.POST, prefix='instructions')
            else:
                data['instructions'] = InstructionFormSet(queryset=RecipeInstruction.objects.none(), prefix='instructions')

        return data

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        
        if 'add_ingredient' in request.POST:
            copy = request.POST.copy()
            copy['ingredients-TOTAL_FORMS'] = int(copy.get('ingredients-TOTAL_FORMS', 0)) + 1
            ingredients = IngredientFormSet(copy, queryset=RecipeIngredient.objects.none(), prefix='ingredients')
            
            instructions = InstructionFormSet(request.POST, queryset=RecipeInstruction.objects.none(), prefix='instructions')
            
            return self.render_to_response(self.get_context_data(form=form, ingredients=ingredients, instructions=instructions))

        if 'add_instruction' in request.POST:
            copy = request.POST.copy()
            copy['instructions-TOTAL_FORMS'] = int(copy.get('instructions-TOTAL_FORMS', 0)) + 1
            instructions = InstructionFormSet(copy, queryset=RecipeInstruction.objects.none(), prefix='instructions')
            
            ingredients = IngredientFormSet(request.POST, queryset=RecipeIngredient.objects.none(), prefix='ingredients')

            return self.render_to_response(self.get_context_data(form=form, ingredients=ingredients, instructions=instructions))

        ingredients = IngredientFormSet(request.POST, prefix='ingredients')
        instructions = InstructionFormSet(request.POST, prefix='instructions')
        
        if form.is_valid() and ingredients.is_valid() and instructions.is_valid():
            return self.form_valid(form, ingredients, instructions)
        else:
            return self.form_invalid(form, ingredients, instructions)

    def form_valid(self, form, ingredients, instructions):
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()
            
            ingredients.instance = self.object
            ingredients.save()
            
            instructions.instance = self.object
            instructions.save()
            
        return super().form_valid(form)

    def form_invalid(self, form, ingredients, instructions):
        return self.render_to_response(
            self.get_context_data(form=form, ingredients=ingredients, instructions=instructions)
        )

    def get_success_url(self):
        messages.success(self.request, "Your recipe has been created woah!")
        return reverse('dashboard')