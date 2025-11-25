"""
Management command to seed the database with demo data.

This command creates a small set of named fixture recipes and then fills up
to ``RECIPE_COUNT`` total recipes using Faker-generated data. Existing records
are left untouched—if a create fails (e.g., due to duplicates), the error
is swallowed and generation continues.
"""


import requests
from faker import Faker
from faker_food import FoodProvider
from random import randint, choices, choice
from django.core.management.base import BaseCommand, CommandError
from django.core.files.base import ContentFile
from recipes.models import Recipe
from recipes.models.user import User
from recipes.constants import RECIPE_FIXTURES, FOOD_SOURCES



class Command(BaseCommand):
    """
    Build automation command to seed the recipes database with data.

    This command inserts a small set of known recipes (``recipe_fixtures``) and then
    repeatedly generates additional random recipes until ``RECIPE_COUNT`` total recipes
    exist in the database. Each generated recipe receives the same default password.

    Attributes:
        RECIPE_COUNT (int): Target total number of recipes in the database.
        help (str): Short description shown in ``manage.py help``.
        faker (Faker): Locale-specific Faker instance used for random data.
    """

    RECIPE_COUNT = 500
    help = 'Seeds the database with sample data'

    def __init__(self, *args, **kwargs):
        """Initialize the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker('en_GB')
        self.faker.add_provider(FoodProvider)

    def handle(self, *args, **options):
        """
        Django entrypoint for the command.

        Runs the full seeding workflow and stores ``self.recipes`` for any
        post-processing or debugging (not required for operation).
        """
        self.create_recipes()
        self.recipes = Recipe.objects.all()

    def create_recipes(self):
        """
        Create fixture recipes and then generate random recipes up to RECIPE_COUNT.

        The process is idempotent in spirit: attempts that fail (e.g., due to
        uniqueness constraints on fields) are ignored and generation continues.
        """
        self.generate_recipe_fixtures()
        self.generate_random_recipes()

    def generate_recipe_fixtures(self):
        """Attempt to create each predefined fixture recipe."""
        for data in RECIPE_FIXTURES:
            self.try_create_recipe(data)

    def generate_random_recipes(self):
        """
        Generate random recipes until the database contains RECIPE_COUNT recipes.

        Prints a simple progress indicator to stdout during generation.
        """
        recipe_count = Recipe.objects.count()
        while  recipe_count < self.RECIPE_COUNT:
            print(f"Seeding recipe {recipe_count}/{self.RECIPE_COUNT}", end='\r')
            self.generate_recipe()
            recipe_count = Recipe.objects.count()
        print("Recipe seeding complete.      ")

    def generate_recipe(self):
        """
        Generate a single random recipe and attempt to insert it.

        Uses Faker for first/last names, then derives a simple username for the author.
        Uses faker-food to generate a random dish name and description
        """
        author = User.objects.order_by('?').first()
        title = self.faker.dish()
        description = self.faker.dish_description()
        prep_time = self.faker.random_int(min=1, max=100)
        servings = self.faker.random_int(min=1, max=50)
        ingredients = create_ingredients(self.faker)
        instructions = self.faker.paragraph()
        created_at = self.faker.date_time_between(start_date='-34y', end_date='now')
        updated_at = self.faker.date_time_between(start_date=created_at, end_date='now')
        tags = create_tags(self.faker)
        img_data = create_image()

        
        
        self.try_create_recipe({
            "author": author,
            "title": title,
            "description": description,
            "prep_time": prep_time,
            "servings": servings,
            "ingredients": ingredients,
            "instructions": instructions,
            "tags": tags,
            "image": img_data,
            "created_at": created_at,
            "updated_at": updated_at
            
        })
       
    def try_create_recipe(self, data):
        """
        Attempt to create a recipe and ignore any errors.

        Args:
            data (dict): Mapping with keys ``author``, ``title``,
                ``description``, ``prep_time``, ``servings``, ``ingredients``,
                ``instructions``, ``tags``,``image``, ``created_at``, and ``updated_at`` 
        """
        try:
            self.create_recipe(data)
        except Exception as e:
            print(f"Failed to create recipe '{data['title']}': {e}")
            pass

    def create_recipe(self, data):
        """
        Create a recipe.

        Args:
            data (dict): Mapping with keys ``author``, ``title``,
                ``description``, ``prep_time``, ``servings``, ``ingredients``,
                ``instructions``, ``tags``,``image``, ``created_at``, and ``updated_at`` 
        """
        recipe = Recipe.objects.create(
            author=data['author'],
            title = data['title'],
            description = data['description'],
            prep_time = data['prep_time'],
            servings = data['servings'],
            ingredients = data['ingredients'],
            instructions = data['instructions'],
            created_at = data['created_at'],
            updated_at = data['updated_at']
        )

        """
        tags is a many-to-many field and hence cannot be set during create()
        hence define down below

        images also can't be set during create()
    
        """
        recipe.tags.set(data['tags'], [])

        recipe.image.save(
            f"recipe_{recipe.id}.jpg",
            ContentFile(data['image']),
            save=True
        )

def create_author_username(first_name, last_name):
    """
    Construct a simple username from first and last names.

    Args:
        first_name (str): Given name.
        last_name (str): Family name.

    Returns:
        str: A username in the form ``@{firstname}{lastname}`` (lowercased).
    """
    return '@' + first_name.lower() + last_name.lower()

def create_ingredients(faker):
    """
    Generate a string of random ingredients
    """
    ingredients=[]
    for i in range(randint(1,15)): 
        ingredients.append(faker.ingredient())

    return ", ".join(ingredients)

def create_tags(faker):
    """
    Generate a random list of tags

    random.choices() signature:
        random.choices(population, weights=None, *, cum_weights=None, k=1)        
    """

    gen_random = [
        faker.ingredient,
        faker.ethnic_category,
        faker.dish,
        faker.measurement,
        faker.spice
    ]

    n = randint(1, 25)
    tags = set(gen() for gen in choices(gen_random, k=n))

    return list(tags)

def create_image():
    img_url = choice(FOOD_SOURCES)
    img_data = requests.get(img_url).content

    return img_data

    