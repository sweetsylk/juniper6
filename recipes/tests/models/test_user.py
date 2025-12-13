"""Unit tests for the User model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from recipes.models import User

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    fixtures = [
        'recipes/tests/fixtures/default_user.json',
        'recipes/tests/fixtures/other_users.json'
    ]

    GRAVATAR_URL = "https://www.gravatar.com/avatar/363c1b0cd64dadffb867236a00e62986"

    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.user2 = User.objects.get(username='@janedoe')
        self.user3 = User.objects.get(username='@petrapickles')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user1.username = ''
        self._assert_user_is_invalid()

    def test_username_can_be_30_characters_long(self):
        self.user1.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user1.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user1.username = second_user.username
        self._assert_user_is_invalid()

    def test_username_must_start_with_at_symbol(self):
        self.user1.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_contain_only_alphanumericals_after_at(self):
        self.user1.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_must_contain_at_least_3_alphanumericals_after_at(self):
        self.user1.username = '@jo'
        self._assert_user_is_invalid()

    def test_username_may_contain_numbers(self):
        self.user1.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_must_contain_only_one_at(self):
        self.user1.username = '@@johndoe'
        self._assert_user_is_invalid()


    def test_first_name_must_not_be_blank(self):
        self.user1.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user1.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user1.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user1.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user1.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user1.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user1.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user1.last_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_email_must_not_be_blank(self):
        self.user1.email = ''
        self._assert_user_is_invalid()

    def test_email_must_be_unique(self):
        second_user = User.objects.get(username='@janedoe')
        self.user1.email = second_user.email
        self._assert_user_is_invalid()

    def test_email_must_contain_username(self):
        self.user1.email = '@example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_at_symbol(self):
        self.user1.email = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain_name(self):
        self.user1.email = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_email_must_contain_domain(self):
        self.user1.email = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_email_must_not_contain_more_than_one_at(self):
        self.user1.email = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_full_name_must_be_correct(self):
        full_name = self.user1.full_name()
        self.assertEqual(full_name, "John Doe")


    def test_default_gravatar(self):
        actual_gravatar_url = self.user1.gravatar()
        expected_gravatar_url = self._gravatar_url(size=120)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_custom_gravatar(self):
        actual_gravatar_url = self.user1.gravatar(size=100)
        expected_gravatar_url = self._gravatar_url(size=100)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def test_mini_gravatar(self):
        actual_gravatar_url = self.user1.mini_gravatar()
        expected_gravatar_url = self._gravatar_url(size=60)
        self.assertEqual(actual_gravatar_url, expected_gravatar_url)

    def _gravatar_url(self, size):
        gravatar_url = f"{UserModelTestCase.GRAVATAR_URL}?size={size}&default=mp"
        return gravatar_url
    
    def test_followers_can_follow_and_unfollow(self):
        """
        Test that users can follow and unfollow other users
        """

        # User2 has no followers at the start
        self.assertFalse(self.user2.followers.exists())

        # user1 follows user2
        self.user1.follow(self.user2)
        self.assertIn(self.user1, self.user2.followers.all())
        self.assertIn(self.user2, self.user1.following.all())  

        # user1 unfollows user2
        self.user1.unfollow(self.user2)
        self.assertNotIn(self.user1, self.user2.followers.all())
        self.assertNotIn(self.user2, self.user1.following.all())

    def test_cannot_follow_self(self):
        """
        Test that a user cannot follow themselves 
        """

        self.user1.follow(self.user1)
        self.assertNotIn(self.user1, self.user1.followers.all())
        self.assertNotIn(self.user1, self.user1.following.all())

    def test_multiple_followers(self):
        """
        Test multiple users following the same user 
        """
        self.user1.follow(self.user2)
        self.user3.follow(self.user2)

        followers = self.user2.followers.all()
        self.assertIn(self.user1, followers)
        self.assertIn(self.user3, followers)
        self.assertEqual(followers.count(), 2)


    def _assert_user_is_valid(self):
        try:
            self.user1.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user1.full_clean()