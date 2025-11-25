from django.test import TestCase
from django.urls import reverse
from django.contrib.admin.sites import AdminSite
from recipes.models import User
from recipes.admin import UserAdmin
from recipes.tests.helpers import LogInTester

class AdminPanelTestCase(TestCase, LogInTester):

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.admin_url = reverse('admin:index')
        self.user = User.objects.get(username='@johndoe')
        self.admin_user = User.objects.create_user(
            username='@admin',
            password='Password123',
            email='admin@example.org',
            is_staff=True,
            is_superuser=True
        )

    def test_admin_url(self):
        self.assertEqual(self.admin_url,'/admin/')

    def test_admin_redirects_when_not_logged_in(self):
        redirect_url = f"/admin/login/?next={self.admin_url}"
        response = self.client.get(self.admin_url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )

    def test_normal_user_cannot_access_admin(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 302)
        redirect_url = f"/admin/login/?next={self.admin_url}"
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200
        )
    
    def test_admin_user_can_access_admin(self):
        self.client.login(username='@admin', password='Password123')
        response = self.client.get(self.admin_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/index.html')
        self.assertContains(response, "Juniper-6 Admin Panel")
        self.assertContains(response, "Welcome to the Juniper-6 Administration Dashboard")

    def test_ban_action_disables_users(self):
        self.client.login(username='@admin', password='Password123')
        site = AdminSite()
        admin_class = UserAdmin(User,site)
        queryset = User.objects.filter(username='@johndoe')
        admin_class.ban_users(request=None,queryset=queryset)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_unban_action_enables_users(self):
        self.client.login(username='@admin', password='Password123')
        self.user.is_active = False
        self.user.save()
        site = AdminSite()
        admin_class = UserAdmin(User,site)
        queryset = User.objects.filter(username='@johndoe')
        admin_class.unban_users(request=None, queryset=queryset)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)