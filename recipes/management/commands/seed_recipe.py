import requests
from faker import Faker
from faker_food import FoodProvider
from random import randint, choices, choice, uniform
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from recipes.models import Recipe, RecipeIngredient, RecipeInstruction, User 
from recipes.constants import RECIPE_FIXTURES, FOOD_SOURCES


class Command(BaseCommand):
    """
    Build automation command to seed the recipes database with data.
    """

    RECIPE_COUNT = 500
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker('en_GB')
        self.faker.add_provider(FoodProvider)

    def handle(self, *args, **options):
        self.create_recipes()
        self.recipes = Recipe.objects.all()

    def create_recipes(self):
        self.generate_recipe_fixtures()
        self.generate_random_recipes()

    def generate_recipe_fixtures(self):
        """Attempt to create each predefined fixture recipe."""
        for data in RECIPE_FIXTURES:
            self.try_create_recipe(data)

    def generate_random_recipes(self):
        recipe_count = Recipe.objects.count()
        while recipe_count < self.RECIPE_COUNT:
            print(f"Seeding recipe {recipe_count}/{self.RECIPE_COUNT}", end='\r')
            self.generate_recipe()
            recipe_count = Recipe.objects.count()
        print("Recipe seeding complete.      ")

    def generate_recipe(self):
        """
        Generate a single random recipe.
        """
        author = User.objects.order_by('?').first()
        title = self.faker.dish()
        description = self.faker.dish_description()
        prep_time = self.faker.random_int(min=5, max=120)
        servings = self.faker.random_int(min=1, max=10)
        
        # UPDATED: Generate a list of separate instruction steps
        instructions_list = [self.faker.sentence() for _ in range(randint(3, 8))]
        
        created_at = self.faker.date_time_between(start_date='-2y', end_date='now')
        updated_at = self.faker.date_time_between(start_date=created_at, end_date='now')
        tags = create_tags(self.faker)
        img_data = create_image()
        
        # NEW: Generate structured ingredient data
        ingredients_list = create_ingredients_list(self.faker)

        self.try_create_recipe({
            "author": author,
            "title": title,
            "description": description,
            "prep_time": prep_time,
            "servings": servings,
            "instructions": instructions_list, # Pass the list
            "tags": tags,
            "image": img_data,
            "created_at": created_at,
            "updated_at": updated_at,
            "ingredients": ingredients_list # Pass the list, not a string
        })
       
    def try_create_recipe(self, data):
        try:
            self.create_recipe(data)
        except Exception as e:
            print(f"Failed to create recipe '{data.get('title', 'Unknown')}': {e}")
            pass

    def create_recipe(self, data):
        """
        Create a recipe and its related ingredients.
        """
        # 1. Extract complex data so we don't pass it to Recipe.create
        ingredients_data = data.pop('ingredients', []) 
        instructions_data = data.pop('instructions', []) # Extract instructions
        tags = data.pop('tags', [])
        image_data = data.pop('image', None)

        # 2. Create the base Recipe
        recipe = Recipe.objects.create(**data)

        # 3. Save Image
        if image_data:
            recipe.image.save(
                f"recipe_{recipe.id}.jpg",
                ContentFile(image_data),
                save=True
            )

        # 4. Set Tags
        recipe.tags.set(tags)

        # 5. Create Instructions (UPDATED)
        if isinstance(instructions_data, str):
            # Fallback for old fixtures: split string by periods
            steps = [s.strip() for s in instructions_data.split('.') if s.strip()]
            for i, step in enumerate(steps, 1):
                RecipeInstruction.objects.create(recipe=recipe, step_number=i, text=step)
        elif isinstance(instructions_data, list):
            # Handle new list format
            for i, step in enumerate(instructions_data, 1):
                RecipeInstruction.objects.create(recipe=recipe, step_number=i, text=step)

        # 6. Create Ingredients (The new part)
        # We check if ingredients_data is a string (old fixtures) or list (new randoms)
        if isinstance(ingredients_data, str):
            # Fallback for old fixtures: split string and use defaults
            items = [x.strip() for x in ingredients_data.split(',')]
            for item in items:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    name=item,
                    amount=1,      # Default amount
                    unit='pcs'     # Default unit
                )
        elif isinstance(ingredients_data, list):
            # Handle the new dictionary format
            for ing in ingredients_data:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    name=ing['name'],
                    amount=ing['amount'],
                    unit=ing['unit']
                )

def create_ingredients_list(faker):
    """
    Generate a list of dictionaries for ingredients.
    Returns: [{'name': 'Salt', 'amount': 10, 'unit': 'g'}, ...]
    """
    ingredients = []
    # Removed 'pcs' to match your model choices
    valid_units = ['g', 'kg', 'ml', 'l', 'cup', 'tbsp', 'tsp'] 
    
    # Generate 3 to 12 ingredients
    for _ in range(randint(3, 12)): 
        ingredients.append({
            'name': faker.ingredient(),
            'amount': randint(1, 500), # Simple integer amounts
            'unit': choice(valid_units)
        })

    return ingredients

def create_tags(faker):
    gen_random = [
        faker.ethnic_category,
        faker.dish,
        faker.measurement,
        faker.spice
    ]
    n = randint(1, 5) # Reduced max tags for sanity
    tags = set(gen().split()[0] for gen in choices(gen_random, k=n))
    return list(tags)

def create_image():
    try:
        img_url = choice(FOOD_SOURCES)
        img_data = requests.get(img_url, timeout=5).content
        return img_data
    except:
        return None # Return None if image fetch fails so script continues also plesae dont add nor remove comments