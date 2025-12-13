from django.test import TestCase
from django.urls import reverse
from recipes.models import User

class FollowUnfollowTests(TestCase):
    """
    Tests for follow/unfollow functionality

    A user can follow another user
    A user can unfollow another user
    After following , the follower appears in the followed user's followers list
    Users cannot follow themselves
    """

    def setUp(self):
        """
        Set up 2 users for follow/unfollow tests
        """

        self.user1 = User.objects.create_user(
            username='@user1', email='user1@test.com', password='password123',
            first_name='User', last_name='One'
        )
        self.user2 = User.objects.create_user(
            username='@user2', email='user2@test.com', password='password123',
            first_name='User', last_name='Two'
        )

    def test_follow_user(self):
        """
        Test that user1 can follow user2 and user1 appears in user2's followers list
        """

        self.client.login(username='@user1', password='password123')
        response = self.client.post(reverse('toggle-follow', args=[self.user2.pk]))
        self.user2.refresh_from_db()
        self.assertIn(self.user1, self.user2.followers.all())

    def test_unfollow_user(self):
        """
        Test that a user can unfollow another user
        """

        # Setup: user1 follows user2
        self.user2.followers.add(self.user1)
        self.client.login(username='@user1', password='password123')

        response = self.client.post(reverse('toggle-follow', args=[self.user2.pk]))

        self.user2.refresh_from_db()
        self.assertNotIn(self.user1, self.user2.followers.all())

    def test_cannot_follow_self(self):
        """
        Test that a user cannot follow themselves
        """
        
        self.client.login(username='@user1', password='password123')
        response = self.client.post(reverse('toggle-follow', args=[self.user1.pk]))
        self.user1.refresh_from_db()
        self.assertNotIn(self.user1, self.user1.followers.all())

    def test_followers_and_following_displayed_on_profile(self):
        """
        Test that the following and followers are displayed on the user's profile page
        """

        # user1 follows user2
        self.user2.followers.add(self.user1)
        self.client.login(username='@user1', password='password123')

        # Check user2's profile shows user1 as a follower
        response = self.client.get(reverse('display_user_profile', args=[self.user2.username]))
        self.assertContains(response, self.user1.username)

        # Check user1's profile shows user2 as following
        response = self.client.get(reverse('display_user_profile', args=[self.user1.username]))
        self.assertContains(response, self.user2.username)
