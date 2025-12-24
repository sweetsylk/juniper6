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
            a, b = (r, self) if self.pk > r.pk else (self, r)
            rs, created = RecipeSimilar.objects.get_or_create(recipe_A=a, recipe_B=b)            
            if not created:
                rs.similarity_score=models.F('similarity_score') + 1
                rs.save()

    def get_similar(self):
        #this will only be called by a paginator (?) that splits into groups anyway 
        #so dont need to limit amount of recipes it return
        #or, we could limit it if we're not gonna do a sort of doomscroll thing lol

        s = Recipe.objects.filter(
            models.Q(simsB__recipe_A=self) | models.Q(simsA__recipe_B=self)
        ).distinct().order_by('-simsA__similarity_score')
        return s
    

class RecipeSimilar(models.Model):
    """Custom through table for 'similar' field"""
    recipe_A = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="simsA")
    recipe_B = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="simsB")
    similarity_score = models.IntegerField(default=1)

    class Meta:
        # if row (A,B,x), do not allow another row (A,B,y)
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
    if created and int(instance.rating)>=4:
        similar_recipes = Recipe.objects.filter(
            reviews__user = instance.user,
            reviews__rating__gte = 4 #rating is >= 4
        ).exclude(pk = instance.recipe.pk) 
        instance.recipe.add_similar(similar_recipes)

        #do we get ALL positively rated? seems a little overkill-ish
        #maybe up to 5 recents? 10? 20?what would be a good number for a 
        #small site vs a big one?