from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("moderation", "0003_initial"),
        ("theses", "0004_thesisreviewhighlight"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ReviewVote",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "value",
                    models.SmallIntegerField(
                        choices=[(-1, "Thumbs down"), (1, "Thumbs up")]
                    ),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "editorial_review",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="moderation.editorialreview",
                    ),
                ),
                (
                    "highlight_review",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="theses.thesisreviewhighlight",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="review_votes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="reviewvote",
            constraint=models.CheckConstraint(
                check=(
                    (
                        models.Q(editorial_review__isnull=False)
                        & models.Q(highlight_review__isnull=True)
                    )
                    | (
                        models.Q(editorial_review__isnull=True)
                        & models.Q(highlight_review__isnull=False)
                    )
                ),
                name="review_vote_exactly_one_target",
            ),
        ),
        migrations.AddConstraint(
            model_name="reviewvote",
            constraint=models.UniqueConstraint(
                condition=models.Q(editorial_review__isnull=False),
                fields=("user", "editorial_review"),
                name="unique_editorial_review_vote_per_user",
            ),
        ),
        migrations.AddConstraint(
            model_name="reviewvote",
            constraint=models.UniqueConstraint(
                condition=models.Q(highlight_review__isnull=False),
                fields=("user", "highlight_review"),
                name="unique_highlight_review_vote_per_user",
            ),
        ),
    ]
