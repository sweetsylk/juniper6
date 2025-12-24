from django.db import models
from django.core.validators import MinValueValidator
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
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
    #created_at = models.DateTimeField()#lets seeder randomise time rather than all being same
    updated_at = models.DateTimeField(auto_now=True)
    saved_by = models.ManyToManyField(User, related_name='saved_recipes', blank=True)
    similar = models.ManyToManyField('self', through='RecipeSimilar', related_name='similars', blank=True, symmetrical=False)

    @property
    def type_name(self):
        return self.__class__.__name__
    
    def __str__(self):
        return self.title
    
    def add_similar(self, recipes):
        for r in recipes:
            a, b = (r, self) if self.pk > r.pk else (self, r)
            rs, created = RecipeSimilar.objects.get_or_create(recipe_A=a, recipe_B=b)            
            if not created:
                rs.update()

    def get_similar(self, lim=100):
        s = Recipe.objects.filter(
            models.Q(simsB__recipe_A=self) | models.Q(simsA__recipe_B=self)
        ).distinct().order_by('-simsA__similarity_score')[:lim]
        return s
    

class RecipeSimilar(models.Model):
    """Custom through table for 'similar' field"""
    recipe_A = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="simsA")
    recipe_B = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="simsB")
    similarity_score = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # if row (A,B,x), do not allow another row (A,B,y)
        constraints =[
            models.UniqueConstraint(fields=['recipe_A','recipe_B'], name="unique_similarities")
        ]
    
    def update (self):
        if self.updated_at <= timezone.now() - timedelta(days=60): 
            self.delete()
            return
        else: 
            self.similarity_score=models.F('similarity_score') + 1
            self.save()
    


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
    

@receiver(models.signals.post_save, sender='recipes.RecipeReview')
def handle_new_review(sender, instance, created, **kwargs):
    if created and int(instance.rating)>=4:
        similar_recipes = Recipe.objects.filter(
            reviews__user = instance.user,
            reviews__rating__gte = 4
        ).exclude(pk = instance.recipe.pk).order_by("-created_at")[:10]
        instance.recipe.add_similar(similar_recipes)