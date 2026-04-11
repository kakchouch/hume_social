from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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
    class SponsorshipStatus(models.TextChoices):
        PENDING = 'pending', 'Pending sponsor validation'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'

    sponsorship_status = models.CharField(
        max_length=10,
        choices=SponsorshipStatus.choices,
        default=SponsorshipStatus.APPROVED,
    )
    contacts = models.ManyToManyField('self', blank=True)

    # Founder status
    is_founder = models.BooleanField(default=False)

    # Reputation metrics
    tag_accuracy_score = models.FloatField(
        default=1.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(2.0)],
    )  # 0-2 scale, 1.0 is neutral

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

    def can_write_theses(self):
        """Users cannot write theses while sponsorship is pending."""
        return self.sponsorship_status != self.SponsorshipStatus.PENDING

    def is_in_contact_with(self, other_user):
        """Return whether this user is already connected with another user."""
        if not other_user or not other_user.pk:
            return False
        return self.contacts.filter(pk=other_user.pk).exists()

    def save(self, *args, **kwargs):
        """Persist tag accuracy score within the documented 0-2 scale."""
        self.tag_accuracy_score = max(0.0, min(2.0, self.tag_accuracy_score))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() or self.username


class ContactRequest(models.Model):
    """A pending request between two users before adding them as contacts."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        ACCEPTED = 'accepted', 'Accepted'
        REJECTED = 'rejected', 'Rejected'

    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_contact_requests',
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='received_contact_requests',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['from_user', 'to_user']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.from_user} -> {self.to_user} ({self.status})'
