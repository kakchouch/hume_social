---
title: "Tags App Reference"
---

# Tags App Reference

Source folder: `src/apps/tags`

## Human-Readable Summary

- Aim of the objects: provide a shared taxonomy for factual/logical/normative issues and track community validation around those labels.
- Broader role: tags are the platform's quality annotation layer, linking thesis quality signals to moderation and ranking.
- Specific role: `Tag` defines label semantics, `TagApplication` records a claim that a label applies to a thesis, and `TagVote` records agreement/disagreement from the community.
- Inputs and outputs:
	- Inputs: selected tag type, thesis linkage, user justification, vote direction, resolver decisions.
	- Outputs: updated tag application status, reputation adjustments for taggers, vote aggregates used by downstream quality logic.

## App Config

### TagsConfig

- Source: `src/apps/tags/apps.py`

## Models

### Tag

- Source: `src/apps/tags/models.py`

Parameters (fields):

- `name: CharField(choices=TagType, unique=True)`
- `description: TextField`

Related:

- Referenced by [ThesisReviewHighlight](/docs/reference/theses/#thesisreviewhighlight)
- Referenced by [TagApplication](/docs/reference/tags/#tagapplication)
- Referenced by [UserFeedPreference.preferred_tags](/docs/reference/feed/#userfeedpreference)

### TagApplication

- Source: `src/apps/tags/models.py`

Parameters (fields):

- `tag: ForeignKey(Tag)`
- `thesis: ForeignKey(MiniThesis, related_name='tags')`
- `applied_by: ForeignKey(User)`
- `justification: TextField`
- `status: CharField(choices=Status)`
- `created_at: DateTimeField(default=timezone.now)`
- `resolved_at: DateTimeField(null=True, blank=True)`
- `resolved_by: ForeignKey(User, null=True, blank=True, related_name='resolved_tags')`
- `upvotes: PositiveIntegerField(default=0)`
- `downvotes: PositiveIntegerField(default=0)`

Methods:

- `tag_type` property
- `is_positive` property
- `resolve(resolver, is_valid=True)`
- `_update_tagger_score(was_correct)`

Related:

- Thesis side: [MiniThesis](/docs/reference/theses/#minithesis)
- User side: [User](/docs/reference/users/#user-inherits-abstractuser)

### TagVote

- Source: `src/apps/tags/models.py`

Parameters (fields):

- `tag_application: ForeignKey(TagApplication, related_name='votes')`
- `voter: ForeignKey(User)`
- `is_upvote: BooleanField()`
- `created_at: DateTimeField(default=timezone.now)`

## URL Endpoints

- Source: `src/apps/tags/urls.py`
- Current state: namespace only, no public routes yet.

## Related Documentation

- [Theses App](/docs/reference/theses/)
- [Feed App](/docs/reference/feed/)
- [Moderation App](/docs/reference/moderation/)
