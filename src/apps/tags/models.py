from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.theses.models import MiniThesis


class Tag(models.Model):
    """Community tags applied to mini-theses."""

    # Tag types
    class TagType(models.TextChoices):
        # Factual tags
        REFERENCE_NEEDED = "factual_reference_needed", "[référence nécessaire]"
        PRIMARY_SOURCE_NEEDED = "factual_primary_needed", "[source primaire requise]"
        CONTESTED_SOURCE = "factual_contested", "[source contestée]"
        DEAD_LINK = "factual_dead_link", "[lien mort]"
        MISINTERPRETED_SOURCE = "factual_misinterpreted", "[source mal interprétée]"

        # Logical tags
        NON_SEQUITUR = "logical_non_sequitur", "[non sequitur]"
        OVERGENERALIZATION = "logical_overgeneralization", "[généralisation abusive]"
        CORRELATION_CAUSATION = "logical_correlation", "[corrélation/causalité]"
        UNDECLARED_WORK = "logical_undeclared", "[travail inédit non déclaré]"

        # Normative tags
        IMPLICIT_PREMISE = "normative_implicit", "[prémisse implicite]"
        CONTRADICTORY_PREMISE = "normative_contradictory", "[prémisse contradictoire]"
        CONCLUSION_EXCEEDS = "normative_exceeds", "[conclusion excède les prémisses]"

    name = models.CharField(max_length=50, choices=TagType.choices, unique=True)
    description = models.TextField(help_text="Explanation of what this tag means")

    def __str__(self):
        return self.get_name_display()


class TagApplication(models.Model):
    """Application of a tag to a mini-thesis."""

    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    thesis = models.ForeignKey(
        MiniThesis, on_delete=models.CASCADE, related_name="tags"
    )
    applied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Justification required
    justification = models.TextField(help_text="Why this tag applies")

    # Status
    class Status(models.TextChoices):
        PENDING = "pending", "Pending Review"
        RESOLVED_POSITIVE = "resolved_positive", "Resolved - Valid"
        RESOLVED_NEGATIVE = "resolved_negative", "Resolved - Invalid"
        DISPUTED = "disputed", "Currently Disputed"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )

    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="resolved_tags",
    )

    # Community voting on tag validity
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["tag", "thesis", "applied_by"]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tag} on {self.thesis} by {self.applied_by}"

    @property
    def tag_type(self):
        """Get the category of the tag (factual/logical/normative)."""
        tag_type = self.tag.name.split("_")[0]
        if tag_type in ["factual", "logical", "normative"]:
            return tag_type
        return "unknown"

    @property
    def is_positive(self):
        """Whether this tag is generally considered positive."""
        # For now, all tags are potentially negative (issues to fix)
        # Could be extended for positive reinforcement tags
        return False

    def resolve(self, resolver, is_valid=True):
        """Resolve the tag application."""
        self.resolved_by = resolver
        self.resolved_at = timezone.now()
        if is_valid:
            self.status = self.Status.RESOLVED_POSITIVE
        else:
            self.status = self.Status.RESOLVED_NEGATIVE
        self.save()

        # Update tagger's accuracy score
        self._update_tagger_score(is_valid)

    def _update_tagger_score(self, was_correct):
        """Update the tagger's accuracy score."""
        tagger = self.applied_by
        # Simple scoring: correct tags increase score, incorrect decrease
        adjustment = 0.1 if was_correct else -0.1
        tagger.tag_accuracy_score = max(
            0, min(2, tagger.tag_accuracy_score + adjustment)
        )
        tagger.save()


class TagVote(models.Model):
    """Community votes on tag applications."""

    tag_application = models.ForeignKey(
        TagApplication, on_delete=models.CASCADE, related_name="votes"
    )
    voter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_upvote = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["tag_application", "voter"]

    def __str__(self):
        vote_type = "upvote" if self.is_upvote else "downvote"
        return f"{vote_type} by {self.voter} on {self.tag_application}"
