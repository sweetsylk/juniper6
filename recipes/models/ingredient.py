from django.db import models
from .recipe import Recipe 

"""
Doing it this way would allow for a dynamic number of ingredients on recipes

shit left to do to impliment fully
    - create Ingredient model and define fields ✓
    - create RecipeIngredient model and define fields ✓
    - update 'instructions' field in recipes table to utilise this model
    - write tests for model functionality
    - create seed_instruction.py 
    - update seed_recipe.py to utilise this model 
    - test model functionality using above two

Was going to add same thing for instructions, but that feels like overkill i think, a TextField() seems to work
fine. Unless down the line we want to add specific istruction formatting or selection or something
(e.g. letting users tick off instructions they have completed as they go)
"""


class Ingredient (models.Model):
    """
    Making a seperate Ingredients table lets us query recipes for specific recipes and hence
    filter them in or out or whatever the user wants

    Categories would also be useful for filtering- e.g. could add popular allergens and hence set profiles 
    to excluse them

    ###### extra functionality idea ######
    - Could add a self-referential 'substitutions' field so users could click/hover on an ingredient and see 
    a little pop up thingy that tells you possible substitutions for that ingredient
    - Substiutions would have to add conversions: "1 tsp light soy = 1/2 tasp dark soy + 1/2 tsp water" e.g.
    - If add that, would also have to add option for creators to specify if some ingredients cannot be 
    substituted for that particular recipe (substitutable = True/False)
    - Would also have to account for this when filtering for allergens or preferences- don't have to exclude 
    a recipe if there are allowex substitutions for the undesired ingredient
    """
    CATEGORY_CHOICES = [
        ('vegetable', 'Vegetable'),
        ('fruit', 'Fruit'),
        ('meat', 'Meat'),
        ('fish', 'Fish')
        ('dairy', 'Dairy'),
        ('carbohydrate', 'Carbohydrate')
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=True, null=True)


class RecipeIngredient(models.Model):
    """
    This table lets us store additional information like quantity and units
    Users inputting units manually avoids us having to add constraints that might cause problems for
    users seeing as it's unlikely we'll think up every possible unit that exists in every cuisine

    note- would be cool to add a conversion thing. e.g ould add button to convert grams to cups for foreign 
    users
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField()
    unit = models.CharField(max_length=100)