from faker import Faker
from random import randint, choice
from django.core.management.base import BaseCommand
from recipes.models import User, Recipe, RecipeReview

REVIEW_COMMENTS = [
    "Loved this recipe!",
    "Really tasty and easy to make.",
    "Turned out great, will make again.",
    "Good recipe, but I adjusted the spices.",
    "Simple and delicious.",
    "My family really enjoyed this.",
    "Not bad, but took longer than expected.",
    "Perfect for a quick meal.",
    "Would definitely recommend this.",
    "Great flavours and clear instructions.",
]

class Command(BaseCommand):
    """
    Management command to seed the database with fake recipe reviews.

    Randomly assigns reviews to existing users and recipes, ensuring
    that each user can only review a given recipe once.
    """

    help = "Seed the database with fake recipe reviews"

    REVIEW_COUNT = 1500

    def __init__(self, *args, **kwargs):
        """Initialise the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        """
        Creates REVIEW_COUNT recipe reviews by randomly pairing users
        with recipes and generating realistic ratings and comments.
        """

        users = list(User.objects.all())
        recipes = list(Recipe.objects.all())

        if not users or not recipes:
            self.stdout.write(self.style.ERROR("Cannot seed reviews: users or recipes missing"))
            return 

        created = 0

        while created < self.REVIEW_COUNT:
            user = choice(users)
            recipe = choice(recipes)

            if RecipeReview.objects.filter(user=user, recipe=recipe).exists():
                continue

            comment = choice(REVIEW_COMMENTS)

            RecipeReview.objects.create(user=user, recipe=recipe, rating=randint(1,5), comment=comment, )

            created += 1
            print(f"Seeding review {created}/{self.REVIEW_COUNT}", end="\r")
    
        self.stdout.write(self.style.SUCCESS("\nReview seeding complete."))          