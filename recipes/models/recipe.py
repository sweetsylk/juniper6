from django.db import models
from django.core.validators import MinValueValidator
from .user import User  
from taggit.managers import TaggableManager

class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.IntegerField(validators=[MinValueValidator(1)])   
    servings = models.IntegerField(validators=[MinValueValidator(1)]) 
    tags = TaggableManager()
    image = models.ImageField(upload_to='recipe_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    saved_by = models.ManyToManyField(User, related_name='saved_recipes', blank=True)

    def __str__(self):
        return self.title

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) 
    amount = models.DecimalField(max_digits=5, decimal_places=2, default = 0, validators=[MinValueValidator(0.01)]) 
    
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


class RecipeInstruction(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='instructions', on_delete=models.CASCADE)
    step_number = models.PositiveIntegerField(default=1)
    text = models.TextField()

    class Meta:
        ordering = ['step_number'] 

    def __str__(self):
        return f"Step {self.step_number}"