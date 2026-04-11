from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.theses.models import MiniThesis


class UserFeedPreference(models.Model):
    """User preferences for feed customization."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    preferred_tags = models.ManyToManyField('tags.Tag', blank=True)
    blocked_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='blocked_by'
    )
    min_rigor_threshold = models.FloatField(
        default=0.0, help_text="Minimum rigor score (0-2)"
    )

    def __str__(self):
        return f"Feed preferences for {self.user}"


class FeedItem(models.Model):
    """Cached feed items for performance."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    thesis = models.ForeignKey(MiniThesis, on_delete=models.CASCADE)

    # Calculated scores
    rigor_score = models.FloatField()
    engagement_score = models.FloatField()
    recency_score = models.FloatField()
    total_score = models.FloatField()

    # Cache metadata
    cached_at = models.DateTimeField(default=timezone.now)
    is_visible = models.BooleanField(default=True)

    class Meta:
        unique_together = ['user', 'thesis']
        ordering = ['-total_score', '-cached_at']

    def __str__(self):
        return f"Feed item: {self.thesis} for {self.user}"

    @classmethod
    def calculate_scores(cls, thesis, user):
        """Calculate all scores for a thesis in a user's feed."""
        # Rigor score (primary)
        rigor_score = thesis.rigor_score

        # Engagement score (secondary)
        engagement_score = min(
            2.0, (thesis.comment_count * 0.1 + thesis.citation_count * 0.2)
        )

        # Recency score (tertiary) - decays over time
        hours_old = (timezone.now() - thesis.created_at).total_seconds() / 3600
        recency_score = max(0, 1.0 - (hours_old / 168))  # 168 hours = 1 week

        # Total score with weights
        total_score = (
            (rigor_score * 0.7) + (engagement_score * 0.2) + (recency_score * 0.1)
        )

        return rigor_score, engagement_score, recency_score, total_score
