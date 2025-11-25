from django.db import models
from .user import User  
from taggit.managers import TaggableManager

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.IntegerField() 
    servings = models.IntegerField() 
    instructions = models.TextField()
    tags = TaggableManager()
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# seperated ingredient into a seperate model 
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    

    amount = models.DecimalField(max_digits=5, decimal_places=2, default = 0) 
    
    UNIT_CHOICES = [
        ('g', 'grams'),
        ('kg', 'kilograms'),
        ('ml', 'milliliters'),
        ('l', 'liters'),
        ('cup', 'cups'),
        ('tbsp', 'tbsp'),
        ('tsp', 'tsp'),
    ]
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='g')

    def __str__(self):
        return f"{self.name} ({self.amount} {self.unit})"