from django.test import TestCase
from apps.users.models import User


class UserModelTest(TestCase):
    """Test cases for the custom User model."""

    def test_user_creation(self):
        """Test that a user can be created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

    def test_user_levels(self):
        """Test user level permissions."""
        reader = User.objects.create_user(
            username='reader', level=User.UserLevel.READER
        )
        commentator = User.objects.create_user(
            username='commentator', level=User.UserLevel.COMMENTATOR
        )
        tagger = User.objects.create_user(
            username='tagger', level=User.UserLevel.TAGGER
        )
        reviewer = User.objects.create_user(
            username='reviewer', level=User.UserLevel.EDITORIAL_REVIEWER
        )

        # Test permissions
        self.assertFalse(reader.can_comment())
        self.assertTrue(commentator.can_comment())
        self.assertTrue(tagger.can_comment())
        self.assertTrue(reviewer.can_comment())

        self.assertFalse(reader.can_tag())
        self.assertFalse(commentator.can_tag())
        self.assertTrue(tagger.can_tag())
        self.assertTrue(reviewer.can_tag())

        self.assertFalse(reader.can_review())
        self.assertFalse(commentator.can_review())
        self.assertFalse(tagger.can_review())
        self.assertTrue(reviewer.can_review())

    def test_tag_accuracy_score_bounds(self):
        """Test that tag accuracy score stays within bounds."""
        user = User.objects.create_user(username='testuser')

        # Test upper bound
        user.bounded_tag_accuracy_score = 3.0
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.tag_accuracy_score, 2.0)

        # Test lower bound
        user.bounded_tag_accuracy_score = -1.0
        user.save()
        user.refresh_from_db()
        self.assertEqual(user.tag_accuracy_score, 0.0)
