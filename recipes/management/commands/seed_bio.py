from faker import Faker
from random import choice
from django.core.management.base import BaseCommand
from recipes.models import User

class Command(BaseCommand):
    """
    Management command to seed user profile information.

    This command populates empty user profile fields such as bio,
    favourite cuisine, cooking level, and dietary style.
    """

    help = "Seed user bios and cooking preferences"

    BIOS = [
        "Home cook who enjoys experimenting with new flavours and easy comfort meals.",
        "I love cooking for friends and family, especially on weekends.",
        "Passionate about simple recipes made with fresh ingredients.",
        "Food lover exploring dishes from different cultures.",
        "Cooking is my creative outlet after a busy day.",
        "Always trying to improve my skills in the kitchen.",
        "Enjoys quick meals during the week and baking on weekends.",
        "Big fan of homemade food and learning new techniques.",
        "Cooking enthusiast who loves recreating classic dishes at home.",
        "I like experimenting with flavours and making everyday meals a little more exciting.",
        "Food lover with a passion for homemade dishes and comfort food.",
    ]

    CUISINES = [
        "Italian",
        "Middle Eastern",
        "Indian",
        "Japanese",
        "Mexican",
        "Mediterranean",
        "Fusion",
        "British",
    ]

    COOKING_LEVELS = [
        "beginner",
        "home_cook",
        "advanced",
    ]

    DIETARY_STYLES = [
        "none",
        "vegetarian",
        "vegan",
        "halal",
        "gluten_free",
    ]

    def __init__(self, *args, **kwargs):
        """Initialise the command with a locale-specific Faker instance."""
        super().__init__(*args, **kwargs)
        self.faker = Faker("en_GB")

    def handle(self, *args, **options):
        """Seed missing profile fields for all users."""

        users = User.objects.all()

        if not users.exists():
            self.stdout.write(self.style.ERROR("No users found to seed."))
            return 
        
        updated = 0

        for user in users:
            changed = False

            if not user.bio:
                user.bio = choice(self.BIOS)
                changed = True 

            if not user.favourite_cuisine:
                user.favourite_cuisine = choice(self.CUISINES)
                changed = True
            
            if not user.cooking_level:
                user.cooking_level = choice(self.COOKING_LEVELS)
                changed = True

            if not user.dietary_style:
                user.dietary_style = choice(self.DIETARY_STYLES)
                changed = True

            if changed:
                user.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Seeded profile data for {updated} users."))