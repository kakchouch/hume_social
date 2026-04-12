---
title: "Theses App Reference"
---

# Theses App Reference

Source folder: `src/apps/theses`

## Human-Readable Summary

- Aim of the objects: represent structured arguments, allow follow-up debate, and provide review surfaces for quality improvement.
- Broader role: this is the domain core; it connects users, tags, editorial review, and feed scoring around thesis content.
- Specific role: `MiniThesis` stores argument structure, `ThesisReviewHighlight` anchors section-level review, `ReviewVote` captures community sentiment, forms normalize author/reviewer input, and views orchestrate list/detail/review workflows.
- Inputs and outputs:
  - Inputs: request query/body data (`q`, pagination, selected text, vote target/value), authored text fields, related objects from users/tags/moderation.
  - Outputs: thesis list/detail/review/form templates, persisted thesis/review/vote records, redirects with workflow feedback messages.

## App Config

### ThesesConfig

- Source: `src/apps/theses/apps.py`
- Purpose: Registers app as `apps.theses`

## Models

### MiniThesis

- Source: `src/apps/theses/models.py`

Parameters (fields):

- `author: ForeignKey(User, related_name='theses')`
- `parent_thesis: ForeignKey(self, null=True, blank=True, related_name='follow_up_theses')`
- `thesis: TextField`
- `facts: TextField`
- `normative_premises: TextField`
- `conclusion: TextField`
- `declared_limits: TextField`
- `created_at: DateTimeField(default=timezone.now)`
- `updated_at: DateTimeField(auto_now=True)`
- `is_published: BooleanField(default=True)`
- `is_featured: BooleanField(default=False)`
- `comment_count: PositiveIntegerField(default=0)`
- `citation_count: PositiveIntegerField(default=0)`

Computed properties:

- `rigor_score`
- `follow_up_count`

Related objects:

- Author is [User]({{< relref "/docs/reference/users.md" >}}#user-inherits-abstractuser)
- Reviews are [EditorialReview]({{< relref "/docs/reference/moderation.md" >}}#editorialreview)
- Tags are [TagApplication]({{< relref "/docs/reference/tags.md" >}}#tagapplication)
- Feed scoring uses [FeedItem.calculate_scores]({{< relref "/docs/reference/feed.md" >}}#feeditem)

### Comment

- Source: `src/apps/theses/models.py`
- Fields: `thesis`, `author`, `content`, `created_at`, `parent`

### Citation

- Source: `src/apps/theses/models.py`
- Fields: `citing_thesis`, `cited_thesis`, `context`

### ThesisReviewHighlight

- Source: `src/apps/theses/models.py`
- Section choices: thesis, facts, normative_premises, conclusion, declared_limits

Fields:

- `thesis: ForeignKey(MiniThesis)`
- `reviewer: ForeignKey(User)`
- `section: CharField(choices=Section)`
- `selected_text: TextField`
- `tag: ForeignKey(tags.Tag)`
- `comment: TextField(blank=True)`
- `created_at: DateTimeField(default=timezone.now)`

### ReviewVote

- Source: `src/apps/theses/models.py`

Fields:

- `user: ForeignKey(User, related_name='review_votes')`
- `editorial_review: ForeignKey(moderation.EditorialReview, null=True, blank=True)`
- `highlight_review: ForeignKey(ThesisReviewHighlight, null=True, blank=True)`
- `value: SmallIntegerField(choices=[-1, +1])`
- `created_at: DateTimeField(default=timezone.now)`
- `updated_at: DateTimeField(auto_now=True)`

Constraints:

- Exactly one target (`editorial_review` xor `highlight_review`)
- One user vote per editorial review
- One user vote per highlight review

## Forms

Source: `src/apps/theses/forms.py`

### MiniThesisForm

- Inherits: `forms.ModelForm`

Parameters (form fields):

- `argument_field`
- `viewing_lens`
- `preset_normative_premises`
- `custom_normative_premises`
- Model-backed fields: `thesis`, `facts`, `normative_premises`, `conclusion`, `declared_limits`

Helpers:

- `get_normative_presets(argument_field, viewing_lens)`
- `get_all_normative_presets()`

Methods:

- `__init__(*args, **kwargs)` dynamic preset choices
- `clean()` combines selected and custom premises into `normative_premises`

### ThesisReviewHighlightForm

- Inherits: `forms.ModelForm`
- Fields: `section`, `selected_text`, `tag`, `comment`
- Method: `clean_selected_text()`

## Views

Source: `src/apps/theses/views.py`

### _render_highlighted_section(content, highlights)

- Purpose: Injects tooltip-highlight spans into thesis text
- Parameters: `content`, `highlights`
- Called by: `thesis_detail`

### thesis_list(request)

- Renders: `templates/theses/thesis_list.html` and HTMX fragment `templates/theses/_thesis_cards.html`
- Query params: `q`, `page`
- Context keys: `page_obj`, `search_query`, `can_write_theses`

### thesis_detail(request, pk)

- Renders: `templates/theses/thesis_detail.html`
- Parameters: `request`, `pk`
- Context keys: `thesis`, `follow_up_theses`, `review_count`, `tag_count`, `highlighted_sections`

### thesis_review(request, pk)

- Renders: `templates/theses/thesis_review.html`
- Parameters: `request`, `pk`
- Actions:
  - add highlight review
  - vote on highlight review
  - vote on editorial review
- Context keys: `thesis`, `tag_applications`, `editorial_reviews`, `highlight_reviews`, `review_highlight_form`, `can_add_highlight_review`

### thesis_create(request, parent_pk=None)

- Renders: `templates/theses/thesis_form.html`
- Parameters: `request`, `parent_pk`
- Context keys: `form`, `title`, `parent_thesis`

### thesis_edit(request, pk)

- Renders: `templates/theses/thesis_form.html`
- Parameters: `request`, `pk`

## URL Endpoints

- Source: `src/apps/theses/urls.py`

Routes:

- `/theses/` -> `thesis_list`
- `/theses/<pk>/` -> `thesis_detail`
- `/theses/<pk>/review/` -> `thesis_review`
- `/theses/create/` -> `thesis_create`
- `/theses/<parent_pk>/follow-up/` -> `thesis_create`
- `/theses/<pk>/edit/` -> `thesis_edit`

## Related Documentation

- [Users App]({{< relref "/docs/reference/users.md" >}})
- [Tags App]({{< relref "/docs/reference/tags.md" >}})
- [Moderation App]({{< relref "/docs/reference/moderation.md" >}})
- [Template contracts]({{< relref "/docs/reference/templates.md" >}})
