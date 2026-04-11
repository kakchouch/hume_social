from django.db import models
from django.conf import settings
from django.utils import timezone


class Sponsorship(models.Model):
    """Sponsorship relationships between users."""

    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sponsorships_given",
    )
    sponsored = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sponsorships_received",
    )

    # Sponsorship details
    message = models.TextField(blank=True, help_text="Optional message from sponsor")
    created_at = models.DateTimeField(default=timezone.now)

    # Status tracking
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        REVOKED = "revoked", "Revoked"
        GRADUATED = "graduated", "Graduated"

    status = models.CharField(
        max_length=10, choices=Status.choices, default=Status.ACTIVE
    )

    # Performance tracking
    sponsor_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        choices=[(i, i) for i in range(1, 6)],
        help_text="Sponsor's rating of the sponsored user (1-5)",
    )

    class Meta:
        unique_together = ["sponsor", "sponsored"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sponsor} sponsors {self.sponsored}"


class FounderCohort(models.Model):
    """Tracks the founding cohort of users."""

    name = models.CharField(max_length=100, default="Cohorte Fondatrice")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Cohort members
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="founder_cohorts"
    )

    # Cohort settings
    max_size = models.PositiveIntegerField(default=150)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

    @property
    def current_size(self):
        return self.members.count()

    def can_add_member(self):
        return self.current_size < self.max_size and self.is_active
