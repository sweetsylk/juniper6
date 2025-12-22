from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from taggit.managers import TaggableManager
from .user import User
"""
    Stores a given recipe 
    One user can have many recipes.
"""
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
    similar = models.ManyToManyField('self', through='RecipeSimilar', related_name='similars', blank=True, symmetrical=False)

    def __str__(self):
        return self.title
    
    def add_similar(self, recipes):
        for r in recipes:
            A, B = min(self.pk, r.pk), max(self.pk, r.pk)
            rs, created = RecipeSimilar.objects.get_or_create(recipe_A_id=A, recipe_B_id=B)            
            if not created:
                rs.similarity_score=models.F('similarity_score') + 1
                rs.save()

    def get_similar(self):
        s = Recipe.objects.filter(
            models.Q(similar_A__recipe_B=self) | models.Q(similar_B__recipe_A=self)
        ).order_by('-similars__similarity_score')
        return s
    

class RecipeSimilar(models.Model):
    """Custom through table for 'similar' field"""
    recipe_A = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="similar_A")
    recipe_B = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="similar_B")
    similarity_score = models.IntegerField(default=0)

    #override save() to normalise ordering for simpler querying
    #is this even necessary? I normalised before passing in??
    def save(self, *args, **kwargs):
        if self.recipe_A.pk > self.recipe_B.pk:
            self.recipe_A, self.recipe_B = self.recipe_B, self.recipe_A
        super().save(*args, **kwargs)

    class Meta:
        # if row (A,B,x), do not make another row (A,B,y)
        constraints =[
            models.UniqueConstraint(fields=['recipe_A','recipe_B'], name="unique_similar_recipes")
        ]


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
    

"""
whenever a post request is made for review instance, post_save signal sent
this reciever function checks if rating was positive (>=4), and queries Recipe
model for x other recipes the same user made positive reviews for, and passes
them to Recipe's add_similar() method
"""
@receiver(models.signals.post_save, sender='recipes.RecipeReview')
def handle_new_review(sender, instance, created, **kwargs):
    if created and instance.rating>=4:
        similar_recipes = Recipe.objects.filter(
            reviews__user = instance.user,
            reviews__rating__gte = 4 #rating is >= 4
        ).exclude(pk = instance.recipe.pk) 
        instance.recipe.add_similar(similar_recipes)