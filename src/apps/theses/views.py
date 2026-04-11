from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from .models import MiniThesis
from .forms import MiniThesisForm, CommentForm


def thesis_list(request):
    """Main feed view with rigor-based ranking."""
    theses = MiniThesis.objects.filter(is_published=True)

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
    })


def thesis_detail(request, pk):
    """Detailed view of a mini-thesis with comments."""
    thesis = get_object_or_404(MiniThesis, pk=pk, is_published=True)
    comments = thesis.comments.filter(parent=None).prefetch_related('replies')

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thesis = thesis
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully.')
            return redirect('theses:detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'theses/thesis_detail.html', {
        'thesis': thesis,
        'comments': comments,
        'form': form,
    })


@login_required
def thesis_create(request):
    """Create a new mini-thesis."""
    if request.method == 'POST':
        form = MiniThesisForm(request.POST)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.author = request.user
            thesis.save()
            messages.success(request, 'Mini-thesis created successfully!')
            return redirect('theses:detail', pk=thesis.pk)
    else:
        form = MiniThesisForm()

    return render(request, 'theses/thesis_form.html', {
        'form': form,
        'title': 'Create Mini-Thesis',
    })


@login_required
def thesis_edit(request, pk):
    """Edit an existing mini-thesis."""
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
