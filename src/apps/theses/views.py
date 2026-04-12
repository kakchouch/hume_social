from django.http import HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe
from apps.moderation.models import EditorialReview
from apps.tags.models import TagApplication

from .models import MiniThesis, ThesisReviewHighlight, ReviewVote
from .forms import MiniThesisForm, ThesisReviewHighlightForm


def _render_highlighted_section(content, highlights):
    """Render a thesis section with hoverable review highlights."""
    if not content:
        return ""

    ranges = []
    for highlight in highlights:
        snippet = (highlight.selected_text or "").strip()
        if not snippet:
            continue

        start_search = 0
        found_range = None
        while True:
            idx = content.find(snippet, start_search)
            if idx == -1:
                break
            end = idx + len(snippet)
            overlaps = any(not (end <= rs or idx >= re) for rs, re, _ in ranges)
            if not overlaps:
                found_range = (idx, end, highlight)
                break
            start_search = idx + 1

        if found_range:
            ranges.append(found_range)

    if not ranges:
        return mark_safe(escape(content).replace("\n", "<br>"))

    ranges.sort(key=lambda item: item[0])
    pieces = []
    cursor = 0
    for start, end, highlight in ranges:
        if cursor < start:
            pieces.append(escape(content[cursor:start]).replace("\n", "<br>"))

        snippet_html = escape(content[start:end]).replace("\n", "<br>")
        tag_html = escape(str(highlight.tag))
        comment_html = (
            escape(highlight.comment).replace("\n", "<br>") if highlight.comment else ""
        )
        tooltip = f"<strong>{tag_html}</strong>"
        if comment_html:
            tooltip += f"<br>{comment_html}"

        pieces.append(
            f'<span class="review-highlight">{snippet_html}<span class="review-tooltip">{tooltip}</span></span>'
        )
        cursor = end

    if cursor < len(content):
        pieces.append(escape(content[cursor:]).replace("\n", "<br>"))

    return mark_safe("".join(pieces))


def thesis_list(request):
    """Main feed view with rigor-based ranking."""
    theses = MiniThesis.objects.filter(is_published=True).select_related(
        "author", "parent_thesis"
    )

    # Apply basic filtering
    search_query = request.GET.get("q")
    if search_query:
        theses = theses.filter(
            Q(thesis__icontains=search_query)
            | Q(facts__icontains=search_query)
            | Q(conclusion__icontains=search_query)
        )

    # Sort by rigor score (simplified for now)
    theses = sorted(theses, key=lambda t: t.rigor_score, reverse=True)

    paginator = Paginator(theses, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "search_query": search_query,
        "can_write_theses": (
            request.user.is_authenticated and request.user.can_write_theses()
        ),
    }

    if getattr(request, "htmx", False):
        return render(request, "theses/_thesis_cards.html", context)

    return render(request, "theses/thesis_list.html", context)


def thesis_detail(request, pk):
    """Detailed content view of a mini-thesis without comments."""
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    thesis = get_object_or_404(MiniThesis, pk=pk, is_published=True)
    follow_up_theses = thesis.follow_up_theses.filter(is_published=True).select_related(
        "author"
    )
    review_count = thesis.reviews.filter(
        status=EditorialReview.Status.PUBLISHED
    ).count()
    tag_count = thesis.tags.count()
    section_highlights = {
        section: [] for section in ThesisReviewHighlight.Section.values
    }
    for highlight in thesis.review_highlights.select_related("tag", "reviewer"):
        section_highlights.setdefault(highlight.section, []).append(highlight)

    highlighted_sections = {
        "thesis": _render_highlighted_section(
            thesis.thesis,
            section_highlights.get(ThesisReviewHighlight.Section.THESIS, []),
        ),
        "facts": _render_highlighted_section(
            thesis.facts,
            section_highlights.get(ThesisReviewHighlight.Section.FACTS, []),
        ),
        "normative_premises": _render_highlighted_section(
            thesis.normative_premises,
            section_highlights.get(
                ThesisReviewHighlight.Section.NORMATIVE_PREMISES, []
            ),
        ),
        "conclusion": _render_highlighted_section(
            thesis.conclusion,
            section_highlights.get(ThesisReviewHighlight.Section.CONCLUSION, []),
        ),
        "declared_limits": _render_highlighted_section(
            thesis.declared_limits,
            section_highlights.get(ThesisReviewHighlight.Section.DECLARED_LIMITS, []),
        ),
    }

    return render(
        request,
        "theses/thesis_detail.html",
        {
            "thesis": thesis,
            "follow_up_theses": follow_up_theses,
            "review_count": review_count,
            "tag_count": tag_count,
            "highlighted_sections": highlighted_sections,
        },
    )


def thesis_review(request, pk):
    """Separate review tab showing tags and published editorial reviews."""
    thesis = get_object_or_404(MiniThesis, pk=pk, is_published=True)

    if request.method == "POST" and not request.user.is_authenticated:
        return redirect(f"{reverse('login')}?next={request.path}")

    form = None
    action = request.POST.get("action") if request.method == "POST" else None

    if request.method == "POST" and action == "vote_review":
        vote_value = request.POST.get("vote")
        target_type = request.POST.get("target_type")
        target_id = request.POST.get("target_id")

        try:
            vote_value = int(vote_value)
            if vote_value not in (
                ReviewVote.VoteValue.UP,
                ReviewVote.VoteValue.DOWN,
            ):
                raise ValueError
        except (TypeError, ValueError):
            messages.error(request, "Invalid vote value.")
            return redirect("theses:review", pk=thesis.pk)

        if target_type == "editorial":
            target_review = get_object_or_404(
                EditorialReview,
                pk=target_id,
                thesis=thesis,
                status=EditorialReview.Status.PUBLISHED,
            )
            ReviewVote.objects.update_or_create(
                user=request.user,
                editorial_review=target_review,
                defaults={"value": vote_value, "highlight_review": None},
            )
        elif target_type == "highlight":
            target_review = get_object_or_404(
                ThesisReviewHighlight,
                pk=target_id,
                thesis=thesis,
            )
            ReviewVote.objects.update_or_create(
                user=request.user,
                highlight_review=target_review,
                defaults={"value": vote_value, "editorial_review": None},
            )
        else:
            messages.error(request, "Invalid vote target.")
            return redirect("theses:review", pk=thesis.pk)

        messages.success(request, "Your vote has been recorded.")
        return redirect("theses:review", pk=thesis.pk)

    can_submit_highlight_review = request.user.is_authenticated and (
        request.user.can_review() or request.user.is_staff or request.user.is_superuser
    )
    if can_submit_highlight_review:
        if request.method == "POST" and action != "vote_review":
            form = ThesisReviewHighlightForm(request.POST)
            if form.is_valid():
                section = form.cleaned_data["section"]
                selected_text = form.cleaned_data["selected_text"]
                if selected_text not in getattr(thesis, section):
                    form.add_error(
                        "selected_text",
                        "The selected text must match content in the chosen thesis section.",
                    )
                else:
                    review_highlight = form.save(commit=False)
                    review_highlight.thesis = thesis
                    review_highlight.reviewer = request.user
                    review_highlight.save()
                    messages.success(request, "Highlighted review segment saved.")
                    return redirect("theses:review", pk=thesis.pk)
        else:
            form = ThesisReviewHighlightForm()
    elif request.method == "POST":
        messages.error(
            request, "Only editorial reviewers can add highlighted review segments."
        )
        return redirect("theses:review", pk=thesis.pk)

    tag_applications = thesis.tags.select_related("tag", "applied_by", "resolved_by")
    editorial_reviews = list(
        thesis.reviews.filter(status=EditorialReview.Status.PUBLISHED).select_related(
            "reviewer"
        )
    )
    highlight_reviews = list(thesis.review_highlights.select_related("tag", "reviewer"))

    editorial_votes = ReviewVote.objects.filter(
        editorial_review__in=editorial_reviews
    ).select_related("user", "editorial_review")
    highlight_votes = ReviewVote.objects.filter(
        highlight_review__in=highlight_reviews
    ).select_related("user", "highlight_review")

    editorial_vote_data = {}
    for vote in editorial_votes:
        data = editorial_vote_data.setdefault(
            vote.editorial_review_id,
            {"score": 0, "voters": [], "user_vote": 0},
        )
        data["score"] += vote.value
        data["voters"].append(f"{vote.user}: {'up' if vote.value > 0 else 'down'}")
        if request.user.is_authenticated and vote.user_id == request.user.id:
            data["user_vote"] = vote.value

    highlight_vote_data = {}
    for vote in highlight_votes:
        data = highlight_vote_data.setdefault(
            vote.highlight_review_id,
            {"score": 0, "voters": [], "user_vote": 0},
        )
        data["score"] += vote.value
        data["voters"].append(f"{vote.user}: {'up' if vote.value > 0 else 'down'}")
        if request.user.is_authenticated and vote.user_id == request.user.id:
            data["user_vote"] = vote.value

    for review in editorial_reviews:
        data = editorial_vote_data.get(
            review.id, {"score": 0, "voters": [], "user_vote": 0}
        )
        review.vote_score = data["score"]
        review.vote_voters = data["voters"]
        review.user_vote = data["user_vote"]

    for review in highlight_reviews:
        data = highlight_vote_data.get(
            review.id, {"score": 0, "voters": [], "user_vote": 0}
        )
        review.vote_score = data["score"]
        review.vote_voters = data["voters"]
        review.user_vote = data["user_vote"]

    return render(
        request,
        "theses/thesis_review.html",
        {
            "thesis": thesis,
            "tag_applications": tag_applications,
            "editorial_reviews": editorial_reviews,
            "highlight_reviews": highlight_reviews,
            "review_highlight_form": form,
            "can_add_highlight_review": can_submit_highlight_review,
        },
    )


@login_required
def thesis_create(request, parent_pk=None):
    """Create a new mini-thesis or a follow-up thesis."""
    if not request.user.can_write_theses():
        messages.error(
            request,
            "You cannot write a thesis until your sponsorship is approved.",
        )
        return redirect("theses:list")

    parent_thesis = None
    if parent_pk is not None:
        parent_thesis = get_object_or_404(MiniThesis, pk=parent_pk, is_published=True)

    if request.method == "POST":
        form = MiniThesisForm(request.POST)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.author = request.user
            thesis.parent_thesis = parent_thesis
            thesis.save()
            if parent_thesis:
                messages.success(request, "Follow-up thesis created successfully!")
            else:
                messages.success(request, "Mini-thesis created successfully!")
            return redirect("theses:detail", pk=thesis.pk)
    else:
        form = MiniThesisForm()

    return render(
        request,
        "theses/thesis_form.html",
        {
            "form": form,
            "title": "Write Follow-Up Thesis"
            if parent_thesis
            else "Create Mini-Thesis",
            "parent_thesis": parent_thesis,
        },
    )


@login_required
def thesis_edit(request, pk):
    """Edit an existing mini-thesis."""
    if not request.user.can_write_theses():
        messages.error(
            request,
            "You cannot edit a thesis until your sponsorship is approved.",
        )
        return redirect("theses:list")

    thesis = get_object_or_404(MiniThesis, pk=pk, author=request.user)

    if request.method == "POST":
        form = MiniThesisForm(request.POST, instance=thesis)
        if form.is_valid():
            form.save()
            messages.success(request, "Mini-thesis updated successfully!")
            return redirect("theses:detail", pk=pk)
    else:
        form = MiniThesisForm(instance=thesis)

    return render(
        request,
        "theses/thesis_form.html",
        {
            "form": form,
            "title": "Edit Mini-Thesis",
        },
    )
