from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("", views.user_list, name="list"),
    # Own profile & GDPR
    path("me/", views.my_profile, name="me"),
    path("me/delete/", views.delete_account, name="delete_account"),
    path("me/data/", views.download_my_data, name="download_my_data"),
    path("me/deleted/", views.account_deleted, name="account_deleted"),
    path("cookie-consent/", views.cookie_consent, name="cookie_consent"),
    # Contact requests
    path("contacts/requests/", views.contact_requests, name="contact_requests"),
    path(
        "contacts/requests/<int:pk>/",
        views.contact_request_decision,
        name="contact_request_decision",
    ),
    path(
        "<int:pk>/contact-request/",
        views.send_contact_request,
        name="send_contact_request",
    ),
    # Sponsorship
    path(
        "sponsorship/requests/", views.sponsorship_requests, name="sponsorship_requests"
    ),
    path(
        "sponsorship/requests/<int:pk>/",
        views.sponsorship_decision,
        name="sponsorship_decision",
    ),
    # Public profile (must come last – generic catch-all)
    path("<int:pk>/", views.user_detail, name="detail"),
]
