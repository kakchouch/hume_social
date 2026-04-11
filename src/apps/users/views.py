from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CustomUserCreationForm
from .models import ContactRequest, User


def landing_page(request):
    """Home page that exposes signup only for anonymous users."""
    form = None

    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('index')
        else:
            form = CustomUserCreationForm()

    return render(request, 'index.html', {'signup_form': form})


def user_list(request):
    """Searchable user directory page."""
    query = (request.GET.get('q') or '').strip()

    users = User.objects.select_related('sponsor').order_by('username')
    if query:
        users = users.filter(
            Q(username__icontains=query)
            | Q(real_name__icontains=query)
            | Q(email__icontains=query)
        )

    return render(
        request,
        'users/user_list.html',
        {
            'users': users,
            'search_query': query,
        },
    )


def user_detail(request, pk):
    """User profile with sponsorship and contact information."""
    profile_user = get_object_or_404(
        User.objects.select_related('sponsor').prefetch_related('sponsored_users', 'contacts'),
        pk=pk,
    )
    contact_state = None
    incoming_request = None

    if request.user.is_authenticated and request.user != profile_user:
        if request.user.is_in_contact_with(profile_user):
            contact_state = 'connected'
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
                contact_state = 'sent'
            elif incoming_request:
                contact_state = 'received'

    return render(
        request,
        'users/user_detail.html',
        {
            'profile_user': profile_user,
            'sponsored_users': profile_user.sponsored_users.all().order_by('username'),
            'contacts': profile_user.contacts.all().order_by('username'),
            'contact_state': contact_state,
            'incoming_request': incoming_request,
        },
    )


@login_required
def send_contact_request(request, pk):
    """Send a contact request to another user from their profile page."""
    if request.method != 'POST':
        return redirect('users:detail', pk=pk)

    recipient = get_object_or_404(User, pk=pk)
    if recipient == request.user:
        return redirect('users:detail', pk=pk)

    if request.user.is_in_contact_with(recipient):
        messages.info(request, 'You are already connected with this user.')
        return redirect('users:detail', pk=pk)

    existing_request = ContactRequest.objects.filter(
        Q(from_user=request.user, to_user=recipient)
        | Q(from_user=recipient, to_user=request.user),
        status=ContactRequest.Status.PENDING,
    ).first()
    if existing_request:
        messages.info(request, 'A contact request is already pending between you.')
        return redirect('users:detail', pk=pk)

    ContactRequest.objects.create(from_user=request.user, to_user=recipient)
    messages.success(request, 'Contact request sent.')
    return redirect('users:detail', pk=pk)


@login_required
def contact_requests(request):
    """List incoming and outgoing contact requests for the current user."""
    incoming_requests = ContactRequest.objects.filter(
        to_user=request.user,
        status=ContactRequest.Status.PENDING,
    ).select_related('from_user')
    outgoing_requests = ContactRequest.objects.filter(
        from_user=request.user,
        status=ContactRequest.Status.PENDING,
    ).select_related('to_user')

    return render(
        request,
        'users/contact_requests.html',
        {
            'incoming_requests': incoming_requests,
            'outgoing_requests': outgoing_requests,
        },
    )


@login_required
def contact_request_decision(request, pk):
    """Accept or reject a received contact request."""
    if request.method != 'POST':
        return redirect('users:contact_requests')

    contact_request = get_object_or_404(
        ContactRequest,
        pk=pk,
        to_user=request.user,
        status=ContactRequest.Status.PENDING,
    )
    decision = request.POST.get('decision')
    if decision == 'accept':
        contact_request.status = ContactRequest.Status.ACCEPTED
        contact_request.save(update_fields=['status', 'updated_at'])
        request.user.contacts.add(contact_request.from_user)
        messages.success(request, 'Contact request accepted.')
    elif decision == 'reject':
        contact_request.status = ContactRequest.Status.REJECTED
        contact_request.save(update_fields=['status', 'updated_at'])
        messages.info(request, 'Contact request rejected.')

    return redirect('users:contact_requests')


@login_required
def sponsorship_requests(request):
    """List pending sponsorship requests for the logged-in sponsor."""
    pending_users = User.objects.filter(
        sponsor=request.user,
        sponsorship_status=User.SponsorshipStatus.PENDING,
    ).order_by('date_joined')

    return render(
        request,
        'users/sponsorship_requests.html',
        {'pending_users': pending_users},
    )


@login_required
def sponsorship_decision(request, pk):
    """Approve or reject sponsorship for a pending sponsored user."""
    if request.method != 'POST':
        return redirect('users:sponsorship_requests')

    sponsored_user = get_object_or_404(
        User,
        pk=pk,
        sponsor=request.user,
        sponsorship_status=User.SponsorshipStatus.PENDING,
    )
    decision = request.POST.get('decision')
    if decision == 'approve':
        sponsored_user.sponsorship_status = User.SponsorshipStatus.APPROVED
        sponsored_user.save(update_fields=['sponsorship_status'])
    elif decision == 'reject':
        sponsored_user.sponsorship_status = User.SponsorshipStatus.REJECTED
        sponsored_user.save(update_fields=['sponsorship_status'])

    return redirect('users:sponsorship_requests')
