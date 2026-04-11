import json

from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.feed.models import FeedItem, UserFeedPreference
from apps.theses.models import MiniThesis

from .forms import CustomUserCreationForm, DeleteAccountForm, UserProfileForm
from .models import ContactRequest, User


def landing_page(request):
    """Home page that exposes signup only for anonymous users."""
    form = None
    feed_items = []
    min_rigor_threshold = 0.0

    if not request.user.is_authenticated:
        if request.method == "POST":
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("index")
        else:
            form = CustomUserCreationForm()
    else:
        preferences, _ = UserFeedPreference.objects.get_or_create(user=request.user)
        blocked_user_ids = preferences.blocked_users.values_list("id", flat=True)
        min_rigor_threshold = preferences.min_rigor_threshold
        theses = (
            MiniThesis.objects.filter(is_published=True)
            .select_related("author", "parent_thesis")
            .exclude(author_id__in=blocked_user_ids)
        )
        for thesis in theses:
            (
                rigor_score,
                engagement_score,
                recency_score,
                total_score,
            ) = FeedItem.calculate_scores(
                thesis,
                request.user,
            )
            if rigor_score < min_rigor_threshold:
                continue
            feed_items.append(
                {
                    "thesis": thesis,
                    "rigor_score": rigor_score,
                    "engagement_score": engagement_score,
                    "recency_score": recency_score,
                    "total_score": total_score,
                }
            )
        feed_items.sort(key=lambda item: item["total_score"], reverse=True)
        feed_items = feed_items[:20]

    return render(
        request,
        "index.html",
        {
            "signup_form": form,
            "feed_items": feed_items,
            "min_rigor_threshold": min_rigor_threshold,
        },
    )


def user_list(request):
    """Searchable user directory page."""
    query = (request.GET.get("q") or "").strip()

    users = User.objects.select_related("sponsor").order_by("username")
    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(real_name__icontains=query)
            | Q(email__icontains=query)
        )

    return render(
        request,
        "users/user_list.html",
        {
            "users": users,
            "search_query": query,
        },
    )


def user_detail(request, pk):
    """User profile with sponsorship and contact information."""
    profile_user = get_object_or_404(
        User.objects.select_related("sponsor").prefetch_related(
            "sponsored_users", "contacts"
        ),
        pk=pk,
    )
    contact_state = None
    incoming_request = None

    if request.user.is_authenticated and request.user != profile_user:
        if request.user.is_in_contact_with(profile_user):
            contact_state = "connected"
        else:
            outgoing_request = ContactRequest.objects.filter(
                from_user=request.user,
                to_user=profile_user,
                status=ContactRequest.Status.PENDING,
            ).first()
            incoming_request = ContactRequest.objects.filter(
                from_user=profile_user,
                to_user=request.user,
                status=ContactRequest.Status.PENDING,
            ).first()
            if outgoing_request:
                contact_state = "sent"
            elif incoming_request:
                contact_state = "received"

    return render(
        request,
        "users/user_detail.html",
        {
            "profile_user": profile_user,
            "sponsored_users": profile_user.sponsored_users.all().order_by("username"),
            "contacts": profile_user.contacts.all().order_by("username"),
            "contact_state": contact_state,
            "incoming_request": incoming_request,
        },
    )


@login_required
def send_contact_request(request, pk):
    """Send a contact request to another user from their profile page."""
    if request.method != "POST":
        return redirect("users:detail", pk=pk)

    recipient = get_object_or_404(User, pk=pk)
    if recipient == request.user:
        return redirect("users:detail", pk=pk)

    if request.user.is_in_contact_with(recipient):
        messages.info(request, "You are already connected with this user.")
        return redirect("users:detail", pk=pk)

    existing_request = ContactRequest.objects.filter(
        Q(from_user=request.user, to_user=recipient)
        | Q(from_user=recipient, to_user=request.user),
        status=ContactRequest.Status.PENDING,
    ).first()
    if existing_request:
        messages.info(request, "A contact request is already pending between you.")
        return redirect("users:detail", pk=pk)

    ContactRequest.objects.create(from_user=request.user, to_user=recipient)
    messages.success(request, "Contact request sent.")
    return redirect("users:detail", pk=pk)


@login_required
def contact_requests(request):
    """List incoming and outgoing contact requests for the current user."""
    incoming_requests = ContactRequest.objects.filter(
        to_user=request.user,
        status=ContactRequest.Status.PENDING,
    ).select_related("from_user")
    outgoing_requests = ContactRequest.objects.filter(
        from_user=request.user,
        status=ContactRequest.Status.PENDING,
    ).select_related("to_user")

    return render(
        request,
        "users/contact_requests.html",
        {
            "incoming_requests": incoming_requests,
            "outgoing_requests": outgoing_requests,
        },
    )


@login_required
def contact_request_decision(request, pk):
    """Accept or reject a received contact request."""
    if request.method != "POST":
        return redirect("users:contact_requests")

    contact_request = get_object_or_404(
        ContactRequest,
        pk=pk,
        to_user=request.user,
        status=ContactRequest.Status.PENDING,
    )
    decision = request.POST.get("decision")
    if decision == "accept":
        contact_request.status = ContactRequest.Status.ACCEPTED
        contact_request.save(update_fields=["status", "updated_at"])
        request.user.contacts.add(contact_request.from_user)
        messages.success(request, "Contact request accepted.")
    elif decision == "reject":
        contact_request.status = ContactRequest.Status.REJECTED
        contact_request.save(update_fields=["status", "updated_at"])
        messages.info(request, "Contact request rejected.")

    return redirect("users:contact_requests")


@login_required
def sponsorship_requests(request):
    """List pending sponsorship requests for the logged-in sponsor."""
    pending_users = User.objects.filter(
        sponsor=request.user,
        sponsorship_status=User.SponsorshipStatus.PENDING,
    ).order_by("date_joined")

    return render(
        request,
        "users/sponsorship_requests.html",
        {"pending_users": pending_users},
    )


@login_required
def sponsorship_decision(request, pk):
    """Approve or reject sponsorship for a pending sponsored user."""
    if request.method != "POST":
        return redirect("users:sponsorship_requests")

    sponsored_user = get_object_or_404(
        User,
        pk=pk,
        sponsor=request.user,
        sponsorship_status=User.SponsorshipStatus.PENDING,
    )
    decision = request.POST.get("decision")
    if decision == "approve":
        sponsored_user.sponsorship_status = User.SponsorshipStatus.APPROVED
        sponsored_user.save(update_fields=["sponsorship_status"])
    elif decision == "reject":
        sponsored_user.sponsorship_status = User.SponsorshipStatus.REJECTED
        sponsored_user.save(update_fields=["sponsorship_status"])

    return redirect("users:sponsorship_requests")


# ---------------------------------------------------------------------------
# Own profile (my profile)
# ---------------------------------------------------------------------------


@login_required
def my_profile(request):
    """The currently logged-in user's own profile with edit capability."""
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("users:me")
    else:
        form = UserProfileForm(instance=request.user)

    return render(
        request,
        "users/my_profile.html",
        {
            "form": form,
            "profile_user": request.user,
            "sponsored_users": request.user.sponsored_users.order_by("username"),
            "contacts": request.user.contacts.order_by("username"),
        },
    )


# ---------------------------------------------------------------------------
# Account deletion (GDPR: right to erasure)
# ---------------------------------------------------------------------------


@login_required
def delete_account(request):
    """
    GET  – show confirmation form.
    POST – validate password, anonymise personal data, deactivate account.

    Personal-data fields are overwritten so the record can remain for
    referential integrity (theses, citations, etc.) while the user is
    no longer identifiable.
    """
    form = DeleteAccountForm(user=request.user)

    if request.method == "POST":
        form = DeleteAccountForm(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            # Logout before modifying the object in the session
            logout(request)

            pk = user.pk
            user.username = f"deleted_{pk}"
            user.email = ""
            user.real_name = ""
            user.bio = ""
            user.linkedin_url = ""
            user.orcid_url = ""
            user.website_url = ""
            user.is_active = False
            user.deletion_requested_at = timezone.now()
            user.set_unusable_password()
            user.save(
                update_fields=[
                    "username",
                    "email",
                    "real_name",
                    "bio",
                    "linkedin_url",
                    "orcid_url",
                    "website_url",
                    "is_active",
                    "deletion_requested_at",
                    "password",
                ]
            )
            return redirect("users:account_deleted")

    return render(request, "users/delete_account_confirm.html", {"form": form})


def account_deleted(request):
    """Simple confirmation page shown after account deletion."""
    return render(request, "users/account_deleted.html")


# ---------------------------------------------------------------------------
# Data portability (GDPR: right to data portability)
# ---------------------------------------------------------------------------


@login_required
def download_my_data(request):
    """Return all personal data as a JSON download."""
    user = request.user

    theses = list(
        user.theses.values(
            "pk",
            "thesis",
            "conclusion",
            "is_published",
            "created_at",
            "updated_at",
        )
    )
    contact_list = list(user.contacts.values("pk", "username", "real_name"))

    sent_requests = list(
        user.sent_contact_requests.values(
            "pk", "to_user__username", "status", "created_at"
        )
    )
    received_requests = list(
        user.received_contact_requests.values(
            "pk", "from_user__username", "status", "created_at"
        )
    )

    payload = {
        "meta": {
            "exported_at": timezone.now().isoformat(),
            "gdpr_info": (
                "This file contains all personal data we hold about you. "
                "You may request erasure by deleting your account from your profile page."
            ),
        },
        "profile": {
            "pk": user.pk,
            "username": user.username,
            "real_name": user.real_name,
            "email": user.email,
            "bio": user.bio,
            "linkedin_url": user.linkedin_url,
            "orcid_url": user.orcid_url,
            "website_url": user.website_url,
            "level": user.level,
            "sponsorship_status": user.sponsorship_status,
            "is_founder": user.is_founder,
            "date_joined": user.date_joined.isoformat(),
            "last_activity_at": user.last_activity_at.isoformat()
            if user.last_activity_at
            else None,
            "cookies_consented_at": user.cookies_consented_at.isoformat()
            if user.cookies_consented_at
            else None,
        },
        "theses": theses,
        "contacts": contact_list,
        "contact_requests_sent": sent_requests,
        "contact_requests_received": received_requests,
    }

    response = JsonResponse(payload, json_dumps_params={"indent": 2, "default": str})
    response["Content-Disposition"] = 'attachment; filename="my_hume_data.json"'
    return response


# ---------------------------------------------------------------------------
# Cookie consent
# ---------------------------------------------------------------------------


@require_POST
def cookie_consent(request):
    """Record cookie consent in session (and on User model if authenticated)."""
    request.session["cookies_consented"] = True
    if request.user.is_authenticated and not request.user.cookies_consented_at:
        User.objects.filter(pk=request.user.pk).update(
            cookies_consented_at=timezone.now()
        )
    next_url = request.POST.get("next") or request.META.get("HTTP_REFERER") or "/"
    return redirect(next_url)
