from django.db import models
from .user import User  
from taggit.managers import TaggableManager

class Recipe(models.Model):
    """
    model for a single recipe.
    """
   
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    
 
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.IntegerField() 
    servings = models.IntegerField()
    ingredients = models.TextField()
    instructions = models.TextField()
    tags = TaggableManager()
    

    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title