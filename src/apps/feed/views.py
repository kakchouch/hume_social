from django.views.generic import TemplateView

from apps.theses.models import MiniThesis

from .models import FeedItem, UserFeedPreference


class FeedHomeView(TemplateView):
    template_name = 'feed/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        theses = MiniThesis.objects.filter(is_published=True).select_related('author')
        min_rigor_threshold = 0.0

        if self.request.user.is_authenticated:
            preferences, _ = UserFeedPreference.objects.get_or_create(user=self.request.user)
            blocked_user_ids = preferences.blocked_users.values_list('id', flat=True)
            theses = theses.exclude(author_id__in=blocked_user_ids)
            min_rigor_threshold = preferences.min_rigor_threshold

        feed_items = []
        for thesis in theses:
            rigor_score, engagement_score, recency_score, total_score = FeedItem.calculate_scores(
                thesis,
                self.request.user if self.request.user.is_authenticated else None,
            )
            if rigor_score < min_rigor_threshold:
                continue
            feed_items.append(
                {
                    'thesis': thesis,
                    'rigor_score': rigor_score,
                    'engagement_score': engagement_score,
                    'recency_score': recency_score,
                    'total_score': total_score,
                }
            )

        feed_items.sort(key=lambda item: item['total_score'], reverse=True)
        context['feed_items'] = feed_items[:20]
        context['min_rigor_threshold'] = min_rigor_threshold
        return context
