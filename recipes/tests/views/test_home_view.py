"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from recipes.models import User

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['recipes/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')

    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

 

def test_get_home_shows_content_when_logged_in(self):
    self.client.login(username=self.user.username, password="Password123")
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, "Recipe")
    self.assertTemplateUsed(response, 'home.html')