from django.test import TestCase
from django.urls import reverse

from apps.moderation.models import EditorialReview
from apps.users.models import User
from apps.tags.models import Tag
from apps.theses.models import (
    MiniThesis,
    Comment,
    Citation,
    ThesisReviewHighlight,
    ReviewVote,
)
from apps.theses.forms import MiniThesisForm


class TestMiniThesisModel(TestCase):
    """Test cases for the MiniThesis model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser")

    def test_mini_thesis_creation(self):
        """Test that a mini-thesis can be created."""
        thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Test thesis proposition",
            facts="Test facts with sources",
            normative_premises="Test normative premises",
            conclusion="Test conclusion",
            declared_limits="Test limits",
        )

        self.assertEqual(thesis.author, self.user)
        self.assertEqual(thesis.thesis, "Test thesis proposition")
        self.assertEqual(thesis.rigor_score, 0.5)  # No tags = neutral score

    def test_rigor_score_calculation(self):
        """Test rigor score calculation with tags."""
        thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Test thesis",
            facts="Test facts",
            normative_premises="Test premises",
            conclusion="Test conclusion",
            declared_limits="Test limits",
        )

        # Without tags, should be 0.5
        self.assertEqual(thesis.rigor_score, 0.5)

    def test_follow_up_count(self):
        thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Base thesis",
            facts="Facts",
            normative_premises="Premises",
            conclusion="Conclusion",
            declared_limits="Limits",
        )
        MiniThesis.objects.create(
            author=self.user,
            parent_thesis=thesis,
            thesis="Follow-up thesis",
            facts="Facts",
            normative_premises="Premises",
            conclusion="Conclusion",
            declared_limits="Limits",
        )

        self.assertEqual(thesis.follow_up_count, 1)


class TestCommentModel(TestCase):
    """Test cases for the Comment model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser")
        self.thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Test thesis",
            facts="Test facts",
            normative_premises="Test premises",
            conclusion="Test conclusion",
            declared_limits="Test limits",
        )

    def test_comment_creation(self):
        """Test that a comment can be created."""
        comment = Comment.objects.create(
            thesis=self.thesis, author=self.user, content="Test comment content"
        )

        self.assertEqual(comment.thesis, self.thesis)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "Test comment content")


class TestCitationModel(TestCase):
    """Test cases for the Citation model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser")
        self.thesis1 = MiniThesis.objects.create(
            author=self.user,
            thesis="Thesis 1",
            facts="Facts 1",
            normative_premises="Premises 1",
            conclusion="Conclusion 1",
            declared_limits="Limits 1",
        )
        self.thesis2 = MiniThesis.objects.create(
            author=self.user,
            thesis="Thesis 2",
            facts="Facts 2",
            normative_premises="Premises 2",
            conclusion="Conclusion 2",
            declared_limits="Limits 2",
        )

    def test_citation_creation(self):
        """Test that a citation can be created."""
        citation = Citation.objects.create(
            citing_thesis=self.thesis1,
            cited_thesis=self.thesis2,
            context="This thesis builds upon the previous work",
        )

        self.assertEqual(citation.citing_thesis, self.thesis1)
        self.assertEqual(citation.cited_thesis, self.thesis2)
        self.assertEqual(citation.context, "This thesis builds upon the previous work")

    def test_unique_citation_constraint(self):
        """Test that duplicate citations are not allowed."""
        Citation.objects.create(
            citing_thesis=self.thesis1,
            cited_thesis=self.thesis2,
            context="First citation",
        )

        with self.assertRaises(Exception):
            Citation.objects.create(
                citing_thesis=self.thesis1,
                cited_thesis=self.thesis2,
                context="Duplicate citation",
            )


class TestMiniThesisForm(TestCase):
    """Test cases for mini-thesis form normative premises behavior."""

    def _base_form_data(self):
        return {
            "thesis": "Thesis proposition",
            "facts": "Facts and sources",
            "conclusion": "Conclusion",
            "declared_limits": "Declared limits",
        }

    def test_form_accepts_custom_normative_premises(self):
        """Custom premises alone should satisfy validation."""
        data = self._base_form_data()
        data.update({"custom_normative_premises": "Human dignity is a baseline value."})

        form = MiniThesisForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIn(
            "Custom normative premises:", form.cleaned_data["normative_premises"]
        )

    def test_form_accepts_preset_normative_premises(self):
        """Preset premises should satisfy validation even with no custom text."""
        data = self._base_form_data()
        data.update(
            {
                "argument_field": "political",
                "viewing_lens": "liberal",
                "preset_normative_premises": [
                    "Political legitimacy requires transparent and accountable institutions.",
                ],
            }
        )

        form = MiniThesisForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIn(
            "Preset normative premises:", form.cleaned_data["normative_premises"]
        )
        self.assertIn("Field: political", form.cleaned_data["normative_premises"])
        self.assertIn("Viewing lens: liberal", form.cleaned_data["normative_premises"])

    def test_form_requires_custom_or_preset_premises(self):
        """At least one normative premise source must be provided."""
        form = MiniThesisForm(data=self._base_form_data())

        self.assertFalse(form.is_valid())
        self.assertIn("custom_normative_premises", form.errors)

    def test_form_accepts_field_without_lens(self):
        """A user can skip lens and still use field presets."""
        data = self._base_form_data()
        data.update(
            {
                "argument_field": "technical",
                "preset_normative_premises": [
                    "Systems should be evaluated through reliability, safety, and maintainability.",
                ],
            }
        )

        form = MiniThesisForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIn("Field: technical", form.cleaned_data["normative_premises"])
        self.assertNotIn("Viewing lens:", form.cleaned_data["normative_premises"])

    def test_form_accepts_new_availability_lens(self):
        """Technical users can choose the availability lens."""
        data = self._base_form_data()
        data.update(
            {
                "argument_field": "technical",
                "viewing_lens": "availability",
                "preset_normative_premises": [
                    "Critical services should prioritize continuity and graceful degradation.",
                ],
            }
        )

        form = MiniThesisForm(data=data)

        self.assertTrue(form.is_valid())
        self.assertIn(
            "Viewing lens: availability", form.cleaned_data["normative_premises"]
        )


class TestThesisAccessControl(TestCase):
    """Test thesis writing restrictions based on sponsorship status."""

    def setUp(self):
        self.sponsor = User.objects.create_user(username="sponsor_user")
        self.pending_user = User.objects.create_user(
            username="pending_writer",
            sponsor=self.sponsor,
            sponsorship_status=User.SponsorshipStatus.PENDING,
        )
        self.approved_user = User.objects.create_user(
            username="approved_writer",
            sponsor=self.sponsor,
            sponsorship_status=User.SponsorshipStatus.APPROVED,
        )

    def test_pending_user_cannot_access_thesis_create(self):
        self.client.force_login(self.pending_user)

        response = self.client.get(reverse("theses:create"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("theses:list"))
        messages = list(response.context["messages"])
        self.assertTrue(
            any(
                "cannot write a thesis until your sponsorship is approved"
                in str(message)
                for message in messages
            )
        )

    def test_approved_user_can_access_thesis_create(self):
        self.client.force_login(self.approved_user)

        response = self.client.get(reverse("theses:create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create Mini-Thesis")


class TestThesisViews(TestCase):
    """Test thesis detail, follow-up creation, and review tab behavior."""

    def setUp(self):
        self.user = User.objects.create_user(username="author")
        self.reviewer = User.objects.create_user(
            username="editor_reviewer",
            level=User.UserLevel.EDITORIAL_REVIEWER,
        )
        self.review_tag = Tag.objects.create(
            name=Tag.TagType.NON_SEQUITUR,
            description="Logical jump between premises and conclusion.",
        )
        self.thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Main thesis",
            facts="Main facts",
            normative_premises="Main premises",
            conclusion="Main conclusion",
            declared_limits="Main limits",
        )

    def test_thesis_detail_rejects_post_requests(self):
        response = self.client.post(reverse("theses:detail", args=[self.thesis.pk]))

        self.assertEqual(response.status_code, 405)

    def test_follow_up_create_sets_parent_thesis(self):
        self.client.force_login(self.user)
        payload = {
            "thesis": "Follow-up argument",
            "facts": "Follow-up facts",
            "conclusion": "Follow-up conclusion",
            "declared_limits": "Follow-up limits",
            "custom_normative_premises": "Follow-up premise",
        }

        response = self.client.post(
            reverse("theses:follow_up", args=[self.thesis.pk]),
            payload,
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        follow_up = MiniThesis.objects.get(thesis="Follow-up argument")
        self.assertEqual(follow_up.parent_thesis, self.thesis)

    def test_review_tab_renders(self):
        response = self.client.get(reverse("theses:review", args=[self.thesis.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Review Workspace")

    def test_thesis_list_marks_follow_up_entries(self):
        MiniThesis.objects.create(
            author=self.user,
            parent_thesis=self.thesis,
            thesis="Nested follow-up thesis",
            facts="Nested facts",
            normative_premises="Nested premises",
            conclusion="Nested conclusion",
            declared_limits="Nested limits",
        )

        response = self.client.get(reverse("theses:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Follow-up to")

    def test_thesis_list_includes_htmx_bootstrap_script(self):
        response = self.client.get(reverse("theses:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "vendor/htmx.min.js")

    def test_thesis_list_htmx_request_returns_fragment_only(self):
        response = self.client.get(
            reverse("theses:list"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "theses/_thesis_cards.html")
        self.assertNotContains(response, "<html")

    def test_thesis_list_sets_security_headers(self):
        response = self.client.get(reverse("theses:list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get("X-Frame-Options"), "DENY")
        self.assertIn(
            "strict-origin-when-cross-origin",
            response.headers.get("Referrer-Policy", ""),
        )

    def test_editorial_reviewer_can_add_highlight_review(self):
        self.client.force_login(self.reviewer)

        response = self.client.post(
            reverse("theses:review", args=[self.thesis.pk]),
            {
                "section": "facts",
                "selected_text": "Main facts",
                "tag": self.review_tag.pk,
                "comment": "This part requires stronger support.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ThesisReviewHighlight.objects.filter(
                thesis=self.thesis,
                selected_text="Main facts",
            ).exists()
        )

    def test_superuser_can_add_highlight_review(self):
        superuser = User.objects.create_superuser(
            username="admin_reviewer",
            email="admin@example.com",
            password="AdminPass!234",
        )
        self.client.force_login(superuser)

        response = self.client.post(
            reverse("theses:review", args=[self.thesis.pk]),
            {
                "section": "conclusion",
                "selected_text": "Main conclusion",
                "tag": self.review_tag.pk,
                "comment": "Admin review note.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ThesisReviewHighlight.objects.filter(
                thesis=self.thesis,
                reviewer=superuser,
                selected_text="Main conclusion",
            ).exists()
        )

    def test_highlight_review_appears_in_thesis_detail_with_tooltip_content(self):
        ThesisReviewHighlight.objects.create(
            thesis=self.thesis,
            reviewer=self.reviewer,
            section="facts",
            selected_text="Main facts",
            tag=self.review_tag,
            comment="Tooltip comment",
        )

        response = self.client.get(reverse("theses:detail", args=[self.thesis.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "review-highlight")
        self.assertContains(response, str(self.review_tag))
        self.assertContains(response, "Tooltip comment")

    def test_authenticated_user_can_vote_on_highlight_review(self):
        voter = User.objects.create_user(username="voter_user")
        highlight = ThesisReviewHighlight.objects.create(
            thesis=self.thesis,
            reviewer=self.reviewer,
            section="facts",
            selected_text="Main facts",
            tag=self.review_tag,
            comment="Needs clearer sourcing.",
        )
        self.client.force_login(voter)

        response = self.client.post(
            reverse("theses:review", args=[self.thesis.pk]),
            {
                "action": "vote_review",
                "target_type": "highlight",
                "target_id": highlight.pk,
                "vote": "1",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ReviewVote.objects.filter(
                user=voter,
                highlight_review=highlight,
                value=ReviewVote.VoteValue.UP,
            ).exists()
        )
        self.assertContains(response, "Score: 1")
        self.assertContains(response, "voter_user: up")

    def test_authenticated_user_can_vote_on_editorial_review(self):
        voter = User.objects.create_user(username="voter_editorial")
        editorial_review = EditorialReview.objects.create(
            thesis=self.thesis,
            reviewer=self.reviewer,
            overall_assessment="Well-structured and concise.",
            strengths="Clear chain of argument.",
            weaknesses="Could cite more primary sources.",
            recommendations="Add source links.",
            rigor_rating=4,
            clarity_rating=4,
            originality_rating=3,
            status=EditorialReview.Status.PUBLISHED,
        )
        self.client.force_login(voter)

        response = self.client.post(
            reverse("theses:review", args=[self.thesis.pk]),
            {
                "action": "vote_review",
                "target_type": "editorial",
                "target_id": editorial_review.pk,
                "vote": "-1",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ReviewVote.objects.filter(
                user=voter,
                editorial_review=editorial_review,
                value=ReviewVote.VoteValue.DOWN,
            ).exists()
        )
        self.assertContains(response, "Score: -1")
        self.assertContains(response, "voter_editorial: down")
