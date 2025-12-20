from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from libgravatar import Gravatar

class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)

    profile_image = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )

    # Free-text biography describing the user's cooking style or interests
    bio = models.TextField(
        blank= True,
        max_length=700,
        help_text="Tell others about your cooking style, inspirations, or favourite flavours."
    )

    # User's preferred cuisine (free text for flexibility)
    favourite_cuisine = models.CharField(
        max_length=50,
        blank=True    
    )

    # Fixed set of cooking experience levels
    COOKING_LEVELS = [
        ("beginner", "Beginner"),
        ("home_cook", "Home Cook"),
        ("advanced", "Advanced"),
    ]

    # User-selected cooking level
    cooking_level = models.CharField(
        max_length=20,
        choices=COOKING_LEVELS,
        blank=True,
        null=True
    )

    # Supported dietary preferences
    DIETARY_STYLES = [
        ("none", "No specific diet"),
        ("vegetarian", "Vegetarian"),
        ("vegan", "Vegan"),
        ("halal", "Halal"),
        ("gluten_free", "Gluten Free"),
    ]

    # User-selected dietary style
    dietary_style = models.CharField(
        max_length=20,
        choices=DIETARY_STYLES,
        blank=True,
        null=True
    )

    # Users who follow this user
    followers = models.ManyToManyField(
        'self',
        symmetrical=False, # following is directional (can follow without being followed back)
        related_name='following',   # the user this user follows
        blank=True
    )

    def follow(self, other_user):
        """Follow another user, cannot follow yourself"""

        if self != other_user:
            other_user.followers.add(self)

    def unfollow(self, other_user):
        """Unfollow a user"""

        other_user.followers.remove(self)

    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'
    
    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url
    
    @property
    def gravatar_url(self):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=150, default='retro')
        return gravatar_url
    
    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""
        
        return self.gravatar(size=60)