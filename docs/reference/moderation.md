# Moderation App Reference

Source folder: [../../src/apps/moderation](../../src/apps/moderation)

## Human-Readable Summary

- Aim of the objects: structure editorial assessments and log moderation interventions over content and users.
- Broader role: moderation is the governance layer that converts community review activity into accountable quality control.
- Specific role: `EditorialReview` captures expert evaluation with ratings and narrative feedback, while `ModerationAction` provides an auditable record of enforcement actions.
- Inputs and outputs:
	- Inputs: thesis references, reviewer/moderator identity, rating values, moderation reasons, action targets.
	- Outputs: published review data consumed by thesis review UI and feed scoring, historical action records for transparency and operations.

## App Config

### ModerationConfig

- Source: [../../src/apps/moderation/apps.py](../../src/apps/moderation/apps.py)

## Models

### EditorialReview

- Source: [../../src/apps/moderation/models.py](../../src/apps/moderation/models.py)

Parameters (fields):

- `thesis: ForeignKey(MiniThesis, related_name='reviews')`
- `reviewer: ForeignKey(User)`
- `overall_assessment: TextField`
- `strengths: TextField(blank=True)`
- `weaknesses: TextField(blank=True)`
- `recommendations: TextField(blank=True)`
- `rigor_rating: PositiveSmallIntegerField(1..5)`
- `clarity_rating: PositiveSmallIntegerField(1..5)`
- `originality_rating: PositiveSmallIntegerField(1..5)`
- `status: CharField(choices=Status)`
- `created_at: DateTimeField(default=timezone.now)`
- `updated_at: DateTimeField(auto_now=True)`

Computed properties:

- `average_rating`

Related:

- Review votes: [ReviewVote](theses.md#reviewvote)
- Displayed on [../../templates/theses/thesis_review.html](../../templates/theses/thesis_review.html)

### ModerationAction

- Source: [../../src/apps/moderation/models.py](../../src/apps/moderation/models.py)

Parameters (fields):

- `action_type: CharField(choices=ActionType)`
- `moderator: ForeignKey(User)`
- `thesis: ForeignKey(MiniThesis, null=True, blank=True)`
- `comment: ForeignKey(theses.Comment, null=True, blank=True)`
- `user: ForeignKey(User, null=True, blank=True, related_name='moderation_actions_taken')`
- `reason: TextField`
- `is_reversible: BooleanField(default=True)`
- `created_at: DateTimeField(default=timezone.now)`

Methods:

- `_get_target_display()`

## URL Endpoints

- Source: [../../src/apps/moderation/urls.py](../../src/apps/moderation/urls.py)
- Current state: namespace only, no public routes yet.

## Related Documentation

- [Theses App](theses.md)
- [Users App](users.md)
