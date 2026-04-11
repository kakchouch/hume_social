from django.db import models
from django.conf import settings
from django.utils import timezone


class MiniThesis(models.Model):
    """Core model for mini-theses - structured argumentative posts."""

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='theses'
    )

    # Core structure
    thesis = models.TextField(help_text="A clear and contestable proposition")
    facts = models.TextField(help_text="Sourced facts with references")
    normative_premises = models.TextField(
        help_text="Declared moral values or postulates"
    )
    conclusion = models.TextField(help_text="Logically derived conclusion")
    declared_limits = models.TextField(
        help_text="What the author acknowledges not covering"
    )

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    # Status
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Engagement metrics
    comment_count = models.PositiveIntegerField(default=0)
    citation_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        thesis_text = str(self.thesis)
        return f"{self.author}'s thesis: {thesis_text[:50]}..."

    @property
    def rigor_score(self):
        """Calculate rigor score based on resolved tags."""
        resolved_tags = self.tags.filter(
            status__in=['resolved_positive', 'resolved_negative']
        )
        if not resolved_tags.exists():
            return 0.5  # Neutral score for untagged theses

        positive_count = resolved_tags.filter(status='resolved_positive').count()
        negative_count = resolved_tags.filter(status='resolved_negative').count()
        total_resolved = resolved_tags.count()

        # Weighted score: positive tags boost, negative tags penalize
        score = (positive_count * 1.2 - negative_count * 1.5) / total_resolved
        return max(0, min(2, score + 1))  # Clamp between 0 and 2


class Comment(models.Model):
    """Comments on mini-theses."""

    thesis = models.ForeignKey(
        MiniThesis, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies'
    )

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.thesis}"


class Citation(models.Model):
    """When one thesis cites another."""

    citing_thesis = models.ForeignKey(
        MiniThesis, on_delete=models.CASCADE, related_name='citations_made'
    )
    cited_thesis = models.ForeignKey(
        MiniThesis, on_delete=models.CASCADE, related_name='citations_received'
    )
    context = models.TextField(help_text="How the citation is used in context")

    class Meta:
        unique_together = ['citing_thesis', 'cited_thesis']

    def __str__(self):
        return f"{self.citing_thesis} cites {self.cited_thesis}"
