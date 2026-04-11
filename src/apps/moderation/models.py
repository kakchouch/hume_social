from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.theses.models import MiniThesis


class EditorialReview(models.Model):
    """Editorial reviews by Editorial Reviewers."""

    thesis = models.ForeignKey(
        MiniThesis, on_delete=models.CASCADE, related_name='reviews'
    )
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Review content
    overall_assessment = models.TextField(help_text="Overall quality assessment")
    strengths = models.TextField(blank=True)
    weaknesses = models.TextField(blank=True)
    recommendations = models.TextField(blank=True)

    # Rating (1-5 scale)
    rigor_rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    clarity_rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    originality_rating = models.PositiveSmallIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )

    # Status
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PUBLISHED = 'published', 'Published'
        REVISION_REQUESTED = 'revision_requested', 'Revision Requested'

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['thesis', 'reviewer']
        ordering = ['-created_at']

    def __str__(self):
        return f"Review of {self.thesis} by {self.reviewer}"

    @property
    def average_rating(self):
        return (self.rigor_rating + self.clarity_rating + self.originality_rating) / 3


class ModerationAction(models.Model):
    """Moderation actions taken on content."""

    class ActionType(models.TextChoices):
        HIDE_THESIS = 'hide_thesis', 'Hide Thesis'
        DELETE_COMMENT = 'delete_comment', 'Delete Comment'
        SUSPEND_USER = 'suspend_user', 'Suspend User'
        WARN_USER = 'warn_user', 'Warn User'

    action_type = models.CharField(max_length=20, choices=ActionType.choices)
    moderator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Target (one of these should be set)
    thesis = models.ForeignKey(
        MiniThesis, null=True, blank=True, on_delete=models.CASCADE
    )
    comment = models.ForeignKey(
        'theses.Comment', null=True, blank=True, on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.CASCADE, related_name='moderation_actions_taken'
    )

    reason = models.TextField()
    is_reversible = models.BooleanField(default=True)

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.action_type} by {self.moderator} on {self._get_target_display()}"

    def _get_target_display(self):
        if self.thesis:
            return f"thesis '{self.thesis.thesis[:30]}...'"
        return f"user {self.user}"
