from django.core.management.base import BaseCommand
from recipes.models import User


class Command(BaseCommand):
    """
    Management command to remove seeded user profile information.

    This command clears user profile fields such as bio, favourite cuisine,
    cooking level, and dietary style. User accounts are preserved.
    """

    help = "Remove seeded user bios and cooking preferences"

    def handle(self, *args, **options):
        users = User.objects.filter(is_staff=False)

        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found to unseed."))
            return
        
        cleared = 0

        for user in users:
            user.bio = ""
            user.favourite_cuisine = ""
            user.cooking_level = None
            user.dietary_style = None
            user.save()
            cleared += 1

        self.stdout.write(self.style.SUCCESS(f"Cleared profile data for {cleared} users."))