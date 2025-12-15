from django.core.management.base import BaseCommand
from recipes.models import RecipeReview

class Command(BaseCommand):
    """
    Management command to remove (unseed) recipe reviews from the database.

    This command deletes all RecipeReview records. It complements the
    corresponding seed command and allows developers to reset review data.
    """

    help = 'Deletes all recipe reviews from the database'

    def handle(self, *args, **options):
        RecipeReview.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS("All recipe reviews deleted.")
        )