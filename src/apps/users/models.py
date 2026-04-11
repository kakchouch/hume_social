from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """Custom user model with Hume-specific fields."""

    # Basic profile
    real_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)

    # Verification
    linkedin_url = models.URLField(blank=True)
    orcid_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)

    # Level system
    class UserLevel(models.TextChoices):
        READER = 'reader', 'Reader'
        COMMENTATOR = 'commentator', 'Commentator'
        TAGGER = 'tagger', 'Tagger'
        EDITORIAL_REVIEWER = 'editorial_reviewer', 'Editorial Reviewer'

    level = models.CharField(
        max_length=20,
        choices=UserLevel.choices,
        default=UserLevel.READER
    )

    # Progression tracking
    level_granted_at = models.DateTimeField(default=timezone.now)
    probation_start = models.DateTimeField(null=True, blank=True)

    # Sponsorship system
    sponsor = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='sponsored_users'
    )

    # Founder status
    is_founder = models.BooleanField(default=False)

    # Reputation metrics
    tag_accuracy_score = models.FloatField(default=1.0)  # 0-2 scale, 1.0 is neutral

    @property
    def bounded_tag_accuracy_score(self):
        """Get tag accuracy score with bounds enforced."""
        return max(0, min(2, self.tag_accuracy_score))

    @bounded_tag_accuracy_score.setter
    def bounded_tag_accuracy_score(self, value):
        """Set tag accuracy score with bounds enforced."""
        self.tag_accuracy_score = max(0, min(2, value))

    def can_comment(self):
        return self.level in [
            self.UserLevel.COMMENTATOR,
            self.UserLevel.TAGGER,
            self.UserLevel.EDITORIAL_REVIEWER
        ]

    def can_tag(self):
        return self.level in [self.UserLevel.TAGGER, self.UserLevel.EDITORIAL_REVIEWER]

    def can_review(self):
        return self.level == self.UserLevel.EDITORIAL_REVIEWER

    def __str__(self):
        return self.get_full_name() or self.username
