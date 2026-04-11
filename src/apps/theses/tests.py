from django.test import TestCase
from apps.users.models import User
from apps.theses.models import MiniThesis, Comment, Citation


class MiniThesisModelTest(TestCase):
    """Test cases for the MiniThesis model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser')

    def test_mini_thesis_creation(self):
        """Test that a mini-thesis can be created."""
        thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Test thesis proposition",
            facts="Test facts with sources",
            normative_premises="Test normative premises",
            conclusion="Test conclusion",
            declared_limits="Test limits"
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
            declared_limits="Test limits"
        )

        # Without tags, should be 0.5
        self.assertEqual(thesis.rigor_score, 0.5)


class CommentModelTest(TestCase):
    """Test cases for the Comment model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser')
        self.thesis = MiniThesis.objects.create(
            author=self.user,
            thesis="Test thesis",
            facts="Test facts",
            normative_premises="Test premises",
            conclusion="Test conclusion",
            declared_limits="Test limits"
        )

    def test_comment_creation(self):
        """Test that a comment can be created."""
        comment = Comment.objects.create(
            thesis=self.thesis,
            author=self.user,
            content="Test comment content"
        )

        self.assertEqual(comment.thesis, self.thesis)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "Test comment content")


class CitationModelTest(TestCase):
    """Test cases for the Citation model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username='testuser')
        self.thesis1 = MiniThesis.objects.create(
            author=self.user,
            thesis="Thesis 1",
            facts="Facts 1",
            normative_premises="Premises 1",
            conclusion="Conclusion 1",
            declared_limits="Limits 1"
        )
        self.thesis2 = MiniThesis.objects.create(
            author=self.user,
            thesis="Thesis 2",
            facts="Facts 2",
            normative_premises="Premises 2",
            conclusion="Conclusion 2",
            declared_limits="Limits 2"
        )

    def test_citation_creation(self):
        """Test that a citation can be created."""
        citation = Citation.objects.create(
            citing_thesis=self.thesis1,
            cited_thesis=self.thesis2,
            context="This thesis builds upon the previous work"
        )

        self.assertEqual(citation.citing_thesis, self.thesis1)
        self.assertEqual(citation.cited_thesis, self.thesis2)
        self.assertEqual(citation.context, "This thesis builds upon the previous work")

    def test_unique_citation_constraint(self):
        """Test that duplicate citations are not allowed."""
        Citation.objects.create(
            citing_thesis=self.thesis1,
            cited_thesis=self.thesis2,
            context="First citation"
        )

        with self.assertRaises(Exception):
            Citation.objects.create(
                citing_thesis=self.thesis1,
                cited_thesis=self.thesis2,
                context="Duplicate citation"
            )
