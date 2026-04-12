---
title: "Users App Reference"
---

# Users App Reference

Source folder: `src/apps/users`

## Human-Readable Summary

- Aim of the objects: manage identity, profile data, social graph (contacts), sponsorship decisions, and GDPR user rights.
- Broader role: this app is the account and trust gateway for the entire platform; it determines who can access advanced actions in other apps.
- Specific role: `User` stores capability state, `ContactRequest` manages relationship workflows, forms validate account/profile operations, and views expose profile/contact/sponsorship/GDPR endpoints.
- Inputs and outputs:
	- Inputs: HTTP request parameters (`q`, `pk`, decision flags), authenticated user context, form fields (signup, profile edits, deletion password), model relations.
	- Outputs: rendered user/index templates, redirects after workflow actions, JSON export payload for portability, persisted user/contact state changes.

## App Config

### UsersConfig

- Source: `src/apps/users/apps.py`
- Purpose: Registers the app as `apps.users`.
- Related: [Theses App]({{< relref "/docs/reference/theses.md" >}}), [Feed App]({{< relref "/docs/reference/feed.md" >}})

## Models

### User (inherits AbstractUser)

- Source: `src/apps/users/models.py`
- Inherits: `django.contrib.auth.models.AbstractUser`

Parameters (fields):

- `real_name: CharField(max_length=255, blank=True)`
- `bio: TextField(blank=True)`
- `linkedin_url: URLField(blank=True)`
- `orcid_url: URLField(blank=True)`
- `website_url: URLField(blank=True)`
- `level: CharField(choices=UserLevel)`
- `level_granted_at: DateTimeField(default=timezone.now)`
- `probation_start: DateTimeField(null=True, blank=True)`
- `sponsor: ForeignKey(User, null=True, blank=True, related_name='sponsored_users')`
- `sponsorship_status: CharField(choices=SponsorshipStatus)`
- `contacts: ManyToManyField(User, blank=True)`
- `is_founder: BooleanField(default=False)`
- `last_activity_at: DateTimeField(null=True, blank=True)`
- `cookies_consented_at: DateTimeField(null=True, blank=True)`
- `deletion_requested_at: DateTimeField(null=True, blank=True)`
- `tag_accuracy_score: FloatField(validators=[0.0..2.0])`

Key methods:

- `can_comment()`
- `can_tag()`
- `can_review()`
- `can_write_theses()`
- `is_in_contact_with(other_user)`
- `save(*args, **kwargs)` (clamps `tag_accuracy_score`)

Related objects:

- Used by [MiniThesis]({{< relref "/docs/reference/theses.md" >}}#minithesis)
- Used by [TagApplication]({{< relref "/docs/reference/tags.md" >}}#tagapplication)
- Used by [EditorialReview]({{< relref "/docs/reference/moderation.md" >}}#editorialreview)
- Used by [Sponsorship]({{< relref "/docs/reference/sponsorship.md" >}}#sponsorship)

### ContactRequest

- Source: `src/apps/users/models.py`

Parameters (fields):

- `from_user: ForeignKey(User, related_name='sent_contact_requests')`
- `to_user: ForeignKey(User, related_name='received_contact_requests')`
- `status: CharField(choices=Status)`
- `created_at: DateTimeField(default=timezone.now)`
- `updated_at: DateTimeField(auto_now=True)`

Related objects:

- Used by `send_contact_request`, `contact_requests`, `contact_request_decision`

## Forms

### CustomUserCreationForm

- Source: `src/apps/users/forms.py`
- Inherits: `UserCreationForm`

Parameters (form fields):

- `username`
- `real_name`
- `email`
- `sponsor_username` (required)

Methods:

- `clean_sponsor_username()` resolves `User` sponsor object
- `save(commit=True)` sets sponsorship to pending

### UserProfileForm

- Source: `src/apps/users/forms.py`
- Inherits: `forms.ModelForm`
- Edits: `real_name`, `bio`, `linkedin_url`, `orcid_url`, `website_url`

### DeleteAccountForm

- Source: `src/apps/users/forms.py`
- Inherits: `forms.Form`

Parameters:

- Constructor: `__init__(*args, user=None, **kwargs)`
- Field: `password`

Methods:

- `clean_password()` authenticates current user password

## Views

Source: `src/apps/users/views.py`

### landing_page(request)

- Renders: `templates/index.html`
- Parameters: `request`
- Context keys: `signup_form`, `feed_items`, `min_rigor_threshold`
- Related: [FeedItem.calculate_scores]({{< relref "/docs/reference/feed.md" >}}#feeditem)

### user_list(request)

- Renders: `templates/users/user_list.html`
- Query params: `q`
- Context keys: `users`, `search_query`

### user_detail(request, pk)

- Renders: `templates/users/user_detail.html`
- Parameters: `request`, `pk`
- Context keys: `profile_user`, `sponsored_users`, `contacts`, `contact_state`, `incoming_request`

### send_contact_request(request, pk)

- POST action endpoint
- Parameters: `request`, `pk`
- Uses: `ContactRequest`

### contact_requests(request)

- Renders: `templates/users/contact_requests.html`
- Context keys: `incoming_requests`, `outgoing_requests`

### contact_request_decision(request, pk)

- POST decision endpoint (`accept` or `reject`)
- Parameters: `request`, `pk`

### sponsorship_requests(request)

- Renders: `templates/users/sponsorship_requests.html`
- Context keys: `pending_users`

### sponsorship_decision(request, pk)

- POST decision endpoint (`approve` or `reject`)
- Parameters: `request`, `pk`

### my_profile(request)

- Renders: `templates/users/my_profile.html`
- Context keys: `form`, `profile_user`, `sponsored_users`, `contacts`

### delete_account(request)

- Renders: `templates/users/delete_account_confirm.html`
- Redirects to: `templates/users/account_deleted.html`

### account_deleted(request)

- Renders: `templates/users/account_deleted.html`

### download_my_data(request)

- Returns JSON payload (GDPR portability)

### cookie_consent(request)

- POST endpoint
- Sets session cookie consent and persists timestamp for authenticated user

## URL Endpoints

- Source: `src/apps/users/urls.py`
- Namespace: `users`

Routes:

- `/users/` -> `user_list`
- `/users/me/` -> `my_profile`
- `/users/me/delete/` -> `delete_account`
- `/users/me/data/` -> `download_my_data`
- `/users/me/deleted/` -> `account_deleted`
- `/users/cookie-consent/` -> `cookie_consent`
- `/users/contacts/requests/` -> `contact_requests`
- `/users/contacts/requests/<pk>/` -> `contact_request_decision`
- `/users/<pk>/contact-request/` -> `send_contact_request`
- `/users/sponsorship/requests/` -> `sponsorship_requests`
- `/users/sponsorship/requests/<pk>/` -> `sponsorship_decision`
- `/users/<pk>/` -> `user_detail`

## Related Documentation

- [Theses App]({{< relref "/docs/reference/theses.md" >}})
- [Template contracts]({{< relref "/docs/reference/templates.md" >}})
