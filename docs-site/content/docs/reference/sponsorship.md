---
title: "Sponsorship App Reference"
---

# Sponsorship App Reference

Source folder: `src/apps/sponsorship`

## Human-Readable Summary

- Aim of the objects: model sponsor relationships and cohort membership constraints.
- Broader role: sponsorship defines trust onboarding and long-term contributor progression boundaries.
- Specific role: `Sponsorship` records one sponsor-to-sponsored relationship with lifecycle state and optional evaluation; `FounderCohort` tracks capped cohort membership and activation state.
- Inputs and outputs:
	- Inputs: sponsor/sponsored user identities, status transitions, optional sponsor ratings, cohort capacity settings.
	- Outputs: persisted sponsorship states and cohort membership checks used by user progression and governance workflows.

## App Config

### SponsorshipConfig

- Source: `src/apps/sponsorship/apps.py`

## Models

### Sponsorship

- Source: `src/apps/sponsorship/models.py`

Parameters (fields):

- `sponsor: ForeignKey(User, related_name='sponsorships_given')`
- `sponsored: ForeignKey(User, related_name='sponsorships_received')`
- `message: TextField(blank=True)`
- `created_at: DateTimeField(default=timezone.now)`
- `status: CharField(choices=Status)`
- `sponsor_rating: PositiveSmallIntegerField(1..5, null=True, blank=True)`

Related:

- User lifecycle status: [User.sponsorship_status]({{< relref "/docs/reference/users.md" >}}#user-inherits-abstractuser)

### FounderCohort

- Source: `src/apps/sponsorship/models.py`

Parameters (fields):

- `name: CharField(max_length=100)`
- `description: TextField(blank=True)`
- `created_at: DateTimeField(default=timezone.now)`
- `members: ManyToManyField(User, related_name='founder_cohorts')`
- `max_size: PositiveIntegerField(default=150)`
- `is_active: BooleanField(default=True)`

Methods:

- `current_size` property
- `can_add_member()`

## URL Endpoints

- Source: `src/apps/sponsorship/urls.py`
- Current state: namespace only, no public routes yet.

## Related Documentation

- [Users App]({{< relref "/docs/reference/users.md" >}})
