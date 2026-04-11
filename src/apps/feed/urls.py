from django.urls import path

from .views import FeedHomeView

app_name = "feed"

urlpatterns = [
    path("", FeedHomeView.as_view(), name="index"),
]
