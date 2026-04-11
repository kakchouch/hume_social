from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.feed.models import UserFeedPreference
from apps.theses.models import MiniThesis
from apps.users.models import User


class TestFeedView(TestCase):
    """Test feed ranking and filtering behavior."""

    def setUp(self):
        self.author = User.objects.create_user(username="author")
        self.viewer = User.objects.create_user(username="viewer")
        self.low_engagement = MiniThesis.objects.create(
            author=self.author,
            thesis="Lower score thesis",
            facts="Facts",
            normative_premises="Premises",
            conclusion="Conclusion",
            declared_limits="Limits",
            comment_count=0,
            citation_count=0,
            created_at=timezone.now() - timedelta(hours=48),
        )
        self.high_engagement = MiniThesis.objects.create(
            author=self.author,
            thesis="Higher score thesis",
            facts="Facts",
            normative_premises="Premises",
            conclusion="Conclusion",
            declared_limits="Limits",
            comment_count=10,
            citation_count=4,
            created_at=timezone.now() - timedelta(hours=2),
        )

    def test_feed_orders_theses_by_total_score(self):
        response = self.client.get(reverse("feed:index"))

        self.assertEqual(response.status_code, 200)
        feed_items = response.context["feed_items"]
        self.assertEqual(feed_items[0]["thesis"], self.high_engagement)
        self.assertEqual(feed_items[1]["thesis"], self.low_engagement)

    def test_feed_applies_min_rigor_threshold_for_user(self):
        preference = UserFeedPreference.objects.create(
            user=self.viewer,
            min_rigor_threshold=0.6,
        )
        self.client.force_login(self.viewer)

        response = self.client.get(reverse("feed:index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["feed_items"], [])
        self.assertEqual(preference.min_rigor_threshold, 0.6)
