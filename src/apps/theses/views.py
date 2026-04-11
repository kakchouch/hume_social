from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from apps.moderation.models import EditorialReview
from apps.tags.models import TagApplication

from .models import MiniThesis
from .forms import MiniThesisForm


def thesis_list(request):
    """Main feed view with rigor-based ranking."""
    theses = MiniThesis.objects.filter(is_published=True).select_related('author', 'parent_thesis')

    # Apply basic filtering
    search_query = request.GET.get('q')
    if search_query:
        theses = theses.filter(
            Q(thesis__icontains=search_query) |
            Q(facts__icontains=search_query) |
            Q(conclusion__icontains=search_query)
        )

    # Sort by rigor score (simplified for now)
    theses = sorted(theses, key=lambda t: t.rigor_score, reverse=True)

    paginator = Paginator(theses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'theses/thesis_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'can_write_theses': (
            request.user.is_authenticated and request.user.can_write_theses()
        ),
    })


def thesis_detail(request, pk):
    """Detailed content view of a mini-thesis without comments."""
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])

    thesis = get_object_or_404(MiniThesis, pk=pk, is_published=True)
    follow_up_theses = thesis.follow_up_theses.filter(is_published=True).select_related('author')
    review_count = thesis.reviews.filter(status=EditorialReview.Status.PUBLISHED).count()
    tag_count = thesis.tags.count()

    return render(request, 'theses/thesis_detail.html', {
        'thesis': thesis,
        'follow_up_theses': follow_up_theses,
        'review_count': review_count,
        'tag_count': tag_count,
    })


def thesis_review(request, pk):
    """Separate review tab showing tags and published editorial reviews."""
    thesis = get_object_or_404(MiniThesis, pk=pk, is_published=True)
    tag_applications = thesis.tags.select_related('tag', 'applied_by', 'resolved_by')
    editorial_reviews = thesis.reviews.filter(
        status=EditorialReview.Status.PUBLISHED
    ).select_related('reviewer')

    return render(
        request,
        'theses/thesis_review.html',
        {
            'thesis': thesis,
            'tag_applications': tag_applications,
            'editorial_reviews': editorial_reviews,
        },
    )


@login_required
def thesis_create(request, parent_pk=None):
    """Create a new mini-thesis or a follow-up thesis."""
    if not request.user.can_write_theses():
        messages.error(
            request,
            'You cannot write a thesis until your sponsorship is approved.',
        )
        return redirect('theses:list')

    parent_thesis = None
    if parent_pk is not None:
        parent_thesis = get_object_or_404(MiniThesis, pk=parent_pk, is_published=True)

    if request.method == 'POST':
        form = MiniThesisForm(request.POST)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.author = request.user
            thesis.parent_thesis = parent_thesis
            thesis.save()
            if parent_thesis:
                messages.success(request, 'Follow-up thesis created successfully!')
            else:
                messages.success(request, 'Mini-thesis created successfully!')
            return redirect('theses:detail', pk=thesis.pk)
    else:
        form = MiniThesisForm()

    return render(request, 'theses/thesis_form.html', {
        'form': form,
        'title': 'Write Follow-Up Thesis' if parent_thesis else 'Create Mini-Thesis',
        'parent_thesis': parent_thesis,
    })


@login_required
def thesis_edit(request, pk):
    """Edit an existing mini-thesis."""
    if not request.user.can_write_theses():
        messages.error(
            request,
            'You cannot edit a thesis until your sponsorship is approved.',
        )
        return redirect('theses:list')

    thesis = get_object_or_404(MiniThesis, pk=pk, author=request.user)

    if request.method == 'POST':
        form = MiniThesisForm(request.POST, instance=thesis)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mini-thesis updated successfully!')
            return redirect('theses:detail', pk=pk)
    else:
        form = MiniThesisForm(instance=thesis)

    return render(request, 'theses/thesis_form.html', {
        'form': form,
        'title': 'Edit Mini-Thesis',
    })
