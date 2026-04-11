from django.views.generic import RedirectView


class FeedHomeView(RedirectView):
    """Legacy feed endpoint now points to homepage feed."""

    pattern_name = "index"
    permanent = False
