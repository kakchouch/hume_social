from django.contrib.auth import get_user_model
from django.utils import timezone


class UpdateLastActivityMiddleware:
    """
    Records the last time an authenticated user performed a request.

    The timestamp is written at most once per calendar day (stored as a session
    key so authenticated users don't incur a DB write on every request).
    """

    SESSION_KEY = '_last_activity_date'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            today = timezone.now().date().isoformat()
            if request.session.get(self.SESSION_KEY) != today:
                request.session[self.SESSION_KEY] = today
                User = get_user_model()
                User.objects.filter(pk=request.user.pk).update(
                    last_activity_at=timezone.now()
                )

        return response
