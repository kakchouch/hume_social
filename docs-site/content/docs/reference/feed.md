---
title: "Feed App Reference"
---

# Feed App Reference

Source folder: `src/apps/feed`

## Human-Readable Summary

- Aim of the objects: customize and rank what each user sees in the argument feed.
- Broader role: feed objects transform thesis/review activity into user-specific discovery order and quality filtering.
- Specific role: `UserFeedPreference` stores filtering and blocking preferences; `FeedItem` stores computed score components; `FeedHomeView` preserves route compatibility by redirecting to the active homepage feed.
- Inputs and outputs:
	- Inputs: user preferences (tags, blocked users, minimum rigor), thesis metadata, review counts, recency values.
	- Outputs: score tuples (`rigor`, `engagement`, `recency`, `total`), ordered feed candidate sets, route-level redirect responses.

## App Config

### FeedConfig

- Source: `src/apps/feed/apps.py`

## Models

### UserFeedPreference

- Source: `src/apps/feed/models.py`

Parameters (fields):

- `user: OneToOneField(User)`
- `preferred_tags: ManyToManyField(tags.Tag, blank=True)`
- `blocked_users: ManyToManyField(User, related_name='blocked_by', blank=True)`
- `min_rigor_threshold: FloatField(default=0.0)`

Related:

- Consumed by `users.views.landing_page`
- Uses [Tag](/docs/reference/tags/#tag)

### FeedItem

- Source: `src/apps/feed/models.py`

Parameters (fields):

- `user: ForeignKey(User)`
- `thesis: ForeignKey(MiniThesis)`
- `rigor_score: FloatField`
- `engagement_score: FloatField`
- `recency_score: FloatField`
- `total_score: FloatField`
- `cached_at: DateTimeField(default=timezone.now)`
- `is_visible: BooleanField(default=True)`

Methods:

- `calculate_scores(thesis, user)`

Related:

- Thesis source: [MiniThesis](/docs/reference/theses/#minithesis)
- Review signal: [EditorialReview](/docs/reference/moderation/#editorialreview)

## Views

### FeedHomeView

- Source: `src/apps/feed/views.py`
- Inherits: `django.views.generic.RedirectView`
- Behavior: redirects to root index route

## URL Endpoints

- Source: `src/apps/feed/urls.py`

Routes:

- `/feed/` -> `FeedHomeView`

## Related Documentation

- [Users App](/docs/reference/users/)
- [Theses App](/docs/reference/theses/)
