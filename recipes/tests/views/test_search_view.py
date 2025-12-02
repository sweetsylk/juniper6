from django.test import TestCase
from django.urls import reverse
from recipes.models import Recipe, User, RecipeIngredient
from taggit.models import Tag
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
        self.users = {
            'user1': User.objects.create(username='user1', email='user1@example.com'),
            'user2': User.objects.create(username='user2', email='user2@example.com'),
            'user3': User.objects.create(username='user3', email='user3@example.com')
        }
        
        # Seed recipes data (We keep ingredients as a string here for easy reading, 
        # but we will process it manually below)
        recipe_data = [
            {
                "author": self.users['user1'],
                "title": "Chicken and Rice",
                "description": "Basic lunch but can be yummy",
                "prep_time": 10,
                "servings": 2,
                "ingredients": "Chicken, Rice", 
                "instructions": "Cook rice, cook and season chicken",
                "created_at": datetime(2025, 11, 16, 15, 28),
                "updated_at": datetime(2025, 11, 17, 19, 12), 
                "tags": ["easy"]
            },
            {
                "author": self.users['user2'],
                "title": "Chicken Salad",
                "description": "Yummy and healthy",
                "prep_time": 10,
                "servings": 5,
                "ingredients": "Chicken, Lettuce, Tomato",
                "instructions": "Wash chicken, Wash salad, cook and season chicken",
                "created_at": datetime(2025, 11, 18, 10, 30),
                "updated_at": datetime(2025, 11, 18, 19, 12), 
                "tags": ["vegan", "easy"]
            },
            {
                "author": self.users['user3'],
                "title": "Fairy Cakes",
                "description": "Sweet treats everyone will love!",
                "prep_time": 20,
                "servings": 24,
                "ingredients": "Flour, Sugar, Butter, Egg, Milk",
                "instructions": "Whisk sugar and butter together, Add eggs, Add milk, Add Flour",
                "created_at": datetime(2025, 10, 25, 12, 0),
                "updated_at": datetime(2025, 10, 25, 19, 0), 
                "tags": ["vegan"]
            },
            {
                "author": self.users['user2'],
                "title": "Cereal",
                "description": "Good lazy breakfast",
                "prep_time": 5,
                "servings": 1,
                "ingredients": "Coco pops, milk",
                "instructions": "Add milk, add cereal",
                "created_at": datetime(2024, 1, 12, 22, 45),
                "updated_at": datetime(2024, 8, 1, 19, 12),
                "tags": []
            }
        ]

        # Create recipes 
        self.recipes = []
        self.tags = {}
        
        for data in recipe_data:
            ingredients_str = data.pop('ingredients')
            tag_names = data.pop('tags')
            recipe = Recipe.objects.create(**data)
            item_names = [x.strip() for x in ingredients_str.split(',')]

            self.recipes.append(recipe)
            
            # Create ingredients
            for name in item_names:
                RecipeIngredient.objects.create(
                    recipe=recipe,
                    name=name,
                    amount=1,    
                    unit='pcs'   
                )

            # Create tags
            for tag_name in tag_names:
                if tag_name not in self.tags:
                    self.tags[tag_name] = Tag.objects.create(name=tag_name)
                recipe.tags.add(self.tags[tag_name])

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
      
        for i in range(20):
            Recipe.objects.create(
                author=self.users['user1'],
                title=f"Extra Recipe {i}",
                description="Extra test recipe",
                prep_time=10,
                servings=1,
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

    def test_search_by_author_username(self):
        """Searching by author's username returns recipes authored by that user."""
        response = self.client.get(reverse('search_results'), {'search': 'user2'})
        self.assertEqual(response.status_code, 200)
    
        
        self.assertContains(response, 'Chicken Salad')
        self.assertContains(response, 'Cereal')
    
        self.assertNotContains(response, 'Chicken and Rice')
        self.assertNotContains(response, 'Fairy Cakes')

    def test_search_by_partial_username(self):
        """Partial username search returns correct results."""
        response = self.client.get(reverse('search_results'), {'search': 'user'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken and Rice')
        self.assertContains(response, 'Chicken Salad')
        self.assertContains(response, 'Fairy Cakes')
        self.assertContains(response, 'Cereal')

    def test_search_nonexistent_username(self):
        """Searching for a username that doesn't exist returns no results."""
        response = self.client.get(reverse('search_results'), {'search': 'nonexistentuser'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')
        
       
        self.assertNotContains(response, 'Chicken and Rice')
        self.assertNotContains(response, 'Chicken Salad')
        self.assertNotContains(response, 'Fairy Cakes')
        self.assertNotContains(response, 'Cereal')

    def test_search_exact_single_tag(self):
        """Searching a tag returns only recipes containing that exact tag."""
        response = self.client.get(reverse('search_results'), {'search': '#vegan'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Chicken Salad')
        self.assertContains(response, 'Fairy Cakes')

        self.assertNotContains(response, 'Chicken and Rice')
        self.assertNotContains(response, 'Cereal')

    def test_search_tag_case_insensitive(self):
        """Tag search should be case-insensitive."""
        response = self.client.get(reverse('search_results'), {'search': '#VeGaN'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Chicken Salad')
        self.assertContains(response, 'Fairy Cakes')

    def test_search_tag_partial_does_not_match(self):
        """Partial tag names should not match."""
        response = self.client.get(reverse('search_results'), {'search': '#veg'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'No recipes found')

    def test_search_multiple_tags_AND_logic(self):
        """Multiple tags should be combined using AND logic (recipe must have ALL tags)."""
        response = self.client.get(reverse('search_results'), {'search': '#vegan #easy'})
        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Chicken Salad')   # Has both vegan & easy
        self.assertNotContains(response, 'Fairy Cakes')  # Only vegan

    def test_search_tags_and_normal_words_combined(self):
        """Tag and normal word searches work together."""
        response = self.client.get(reverse('search_results'), {'search': '#vegan Chicken'})
        self.assertEqual(response.status_code, 200)

        # Chicken Salad is vegan and matches "Chicken"
        self.assertContains(response, 'Chicken Salad')

        # Fairy Cakes is vegan but does NOT match "Chicken"
        self.assertNotContains(response, 'Fairy Cakes')

    # FAILED TESTS BELOW - TO BE FIXED
    def test_normal_term_search_with_invalid_tag(self):
        """Normal word search still works even if tag part matches nothing."""
        response = self.client.get(reverse('search_results'), {'search': '#nonexistent Chicken'})
        self.assertEqual(response.status_code, 200)

        # Chicken results still appear
        self.assertContains(response, 'Chicken and Rice')
        self.assertContains(response, 'Chicken Salad')

    def test_tag_search_different_order_existing_tags(self):
        """Multiple tags should match regardless of order for existing recipes."""
        # Chicken Salad has tags: "vegan" and "easy"
        response = self.client.get(reverse('search_results'), {'search': '#vegan #easy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Salad')

        response = self.client.get(reverse('search_results'), {'search': '#easy #vegan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Salad')

    def test_tag_search_nonexistent_tag_combination_existing(self):
        """Searching with one valid tag and one nonexistent tag returns no results."""
        response = self.client.get(reverse('search_results'), {'search': '#vegan #nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')

    def test_tag_search_case_insensitive_existing(self):
        """Tag search is case-insensitive for existing recipes."""
        response = self.client.get(reverse('search_results'), {'search': '#VeGaN #EaSy'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chicken Salad')


