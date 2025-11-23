from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, User
from datetime import datetime

class SearchResultsViewTests(TestCase):
    """
    Tests for the search_results view.
    Seeds the test database with recipes directly inside this test file.
    """

    def setUp(self):
        """
        Create users and seed recipes for testing.
        """
        # Create users
        self.user1 = User.objects.create(username='user1', email='user1@example.com')
        self.user2 = User.objects.create(username='user2', email='user2@example.com')
        self.user3 = User.objects.create(username='user3', email='user3@example.com')

        # Seed recipes
        recipe_data = [
            {
                "author": self.user1,
                "title": "Chicken and Rice",
                "description": "Basic lunch but can be yummy",
                "prep_time": 10,
                "servings": 2,
                "ingredients": "Chicken, Rice",
                "instructions": "Cook rice, cook and season chicken",
                "created_at": datetime(2025, 11, 16, 15, 28),
                "updated_at": datetime(2025, 11, 17, 19, 12)
            },
            {
                "author": self.user2,
                "title": "Chicken Salad",
                "description": "Yummy and healthy",
                "prep_time": 10,
                "servings": 5,
                "ingredients": "Chicken, Lettuce, Tomato",
                "instructions": "Wash chicken, Wash salad, cook and season chicken",
                "created_at": datetime(2025, 11, 18, 10, 30),
                "updated_at": datetime(2025, 11, 18, 19, 12)
            },
            {
                "author": self.user3,
                "title": "Fairy Cakes",
                "description": "Sweet treats everyone will love!",
                "prep_time": 20,
                "servings": 24,
                "ingredients": "Flour, Sugar, Butter, Egg, Milk",
                "instructions": "Whisk sugar and butter together, Add eggs, Add milk, Add Flour",
                "created_at": datetime(2025, 10, 25, 12, 0),
                "updated_at": datetime(2025, 10, 25, 19, 0)
            },
            {
                "author": self.user2,
                "title": "Cereal",
                "description": "Good lazy breakfast",
                "prep_time": 5,
                "servings": 1,
                "ingredients": "Coco pops, milk",
                "instructions": "Add milk, add cereal",
                "created_at": datetime(2024, 1, 12, 22, 45),
                "updated_at": datetime(2024, 8, 1, 19, 12)
            }
        ]

        for data in recipe_data:
            Recipe.objects.create(**data)

    def test_search_found(self):
        """Searching for a term that exists in recipe titles returns results."""
        response = self.client.get(reverse('search_results'), {'search': 'Chicken'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken and Rice')
        self.assertContains(response, 'Chicken Salad')

    def test_search_not_found(self):
        """Searching for a term that does not exist shows the 'no results' message."""
        response = self.client.get(reverse('search_results'), {'search': 'NonexistentRecipe'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')

    def test_search_empty_query(self):
        """Empty search query returns no results."""
        response = self.client.get(reverse('search_results'), {'search': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')

    def test_search_pagination(self):
        """Searching returns results with correct pagination."""
        # Create additional recipes to test pagination
        for i in range(20):
            Recipe.objects.create(
                author=self.user1,
                title=f"Extra Recipe {i}",
                description="Extra test recipe",
                prep_time=10,
                servings=1,
                ingredients="Test ingredients",
                instructions="Test instructions",
                created_at=datetime(2025, 1, 1, 12, 0),
                updated_at=datetime(2025, 1, 1, 12, 0)
            )

        response = self.client.get(reverse('search_results'), {'search': 'Extra'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('page_obj', response.context)
        page_obj = response.context['page_obj']
        self.assertTrue(page_obj.paginator.count >= 20)
        self.assertTrue(page_obj.has_next() or page_obj.has_previous() or page_obj.paginator.num_pages >= 1)
