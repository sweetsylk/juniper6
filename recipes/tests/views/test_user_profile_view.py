from django.test import TestCase
from django.urls import reverse
from recipes.models import User
from recipes.tests.helpers import reverse_with_next
from recipes.tests.helpers import LogInTester

class UserProfileViewTestCase(TestCase, LogInTester):
    
    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile_view')

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/view/')

    def test_get_profile_view_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in',self.url)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )
    
    def test_get_profile_view_logged_in(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile_view.html')
        self.assertEqual(response.context['object'],self.user)
        self.assertEqual(response.context['profile_user'],self.user)