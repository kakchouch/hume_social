# Expert Reference

## 1. System Overview

Hume Social is a server-rendered Django platform with selective HTMX enhancement.
Primary domain object is MiniThesis; trust and quality layers are applied through sponsorship, tagging, and editorial review.

## 2. Technology Stack (Detailed)

- Runtime: Python 3.12.
- Web framework: Django 4.2.
- API package present: djangorestframework.
- Progressive enhancement: django-htmx + htmx 2.0.4 (self-hosted static asset).
- Security headers/CSP: django-csp + Django security settings.
- Database adapters: SQLite default in codebase; psycopg2-binary for PostgreSQL usage.
- Testing: pytest, Django TestCase, project-level tests in src/apps and tests/.

## 3. URL Topology

Root router (src/config/urls.py):

- / -> users.landing_page
- /signin/ -> Django LoginView with custom template
- /logout/ -> Django LogoutView
- /admin/
- /users/ -> apps.users.urls
- /theses/ -> apps.theses.urls
- /tags/ -> apps.tags.urls (placeholder routes)
- /moderation/ -> apps.moderation.urls (placeholder routes)
- /feed/ -> apps.feed.urls
- /sponsorship/ -> apps.sponsorship.urls (placeholder routes)

## 4. App Inventory

### 4.1 users app

Purpose: authentication-adjacent user domain, profiles, sponsorship decisions, contacts, GDPR, landing page.

- Models:
  - User
  - ContactRequest
- Forms:
  - CustomUserCreationForm
  - UserProfileForm
  - DeleteAccountForm
- Views:
  - landing_page
  - user_list
  - user_detail
  - send_contact_request
  - contact_requests
  - contact_request_decision
  - sponsorship_requests
  - sponsorship_decision
  - my_profile
  - delete_account
  - account_deleted
  - download_my_data
  - cookie_consent
- Middleware:
  - UpdateLastActivityMiddleware
- Management command:
  - purge_inactive_users
- URLs:
  - list, me, GDPR endpoints, contact request endpoints, sponsorship endpoints, detail
- Templates consumed:
  - templates/index.html
  - templates/users/*.html

### 4.2 theses app

Purpose: core argument lifecycle and review display.

- Models:
  - MiniThesis
  - Comment
  - Citation
  - ThesisReviewHighlight
- Forms:
  - MiniThesisForm
  - ThesisReviewHighlightForm
- Views:
  - thesis_list
  - thesis_detail
  - thesis_review
  - thesis_create
  - thesis_edit
- URLs:
  - list/detail/review/create/follow_up/edit
- Templates consumed:
  - templates/theses/thesis_list.html
  - templates/theses/_thesis_cards.html
  - templates/theses/thesis_detail.html
  - templates/theses/thesis_review.html
  - templates/theses/thesis_form.html

### 4.3 tags app

Purpose: taxonomy and community validation primitives.

- Models:
  - Tag
  - TagApplication
  - TagVote
- URLs:
  - app namespace defined, no concrete path entries yet.

### 4.4 moderation app

Purpose: editorial review + moderation audit action records.

- Models:
  - EditorialReview
  - ModerationAction
- URLs:
  - app namespace defined, no concrete path entries yet.

### 4.5 feed app

Purpose: feed preferences and ranking cache/calculation.

- Models:
  - UserFeedPreference
  - FeedItem
- Views:
  - FeedHomeView (redirects to index)
- URLs:
  - /feed/ mapped to FeedHomeView
- Template under app:
  - src/apps/feed/templates/feed/index.html (legacy feed presentation)

### 4.6 sponsorship app

Purpose: sponsorship relationship history and founder cohort modeling.

- Models:
  - Sponsorship
  - FounderCohort
- URLs:
  - app namespace defined, no concrete path entries yet.

## 5. Model Catalog

### User

Key fields:

- identity: username, email, real_name, bio
- external profile links: linkedin_url, orcid_url, website_url
- capability: level (reader/commentator/tagger/editorial_reviewer)
- sponsorship: sponsor, sponsorship_status
- network: contacts (self many-to-many)
- reputation: tag_accuracy_score bounded to [0, 2]
- compliance/activity: last_activity_at, cookies_consented_at, deletion_requested_at

Key methods:

- can_comment, can_tag, can_review
- can_write_theses
- is_in_contact_with
- bounded_tag_accuracy_score property + save clamp

### ContactRequest

- directed request from from_user to to_user
- statuses: pending, accepted, rejected
- unique per user pair

### MiniThesis

- content fields: thesis, facts, normative_premises, conclusion, declared_limits
- threading: parent_thesis for follow-up chains
- computed properties: rigor_score, follow_up_count

### Comment

- threaded comments via parent self-FK

### Citation

- many-to-many through table between theses with context

### ThesisReviewHighlight

- reviewer-selected exact text segment tied to section + tag + optional comment

### Tag

- predefined taxonomy as TagType choices

### TagApplication

- application metadata + voting totals + resolver fields
- resolve() updates status and tagger score

### TagVote

- one vote per voter per tag application

### EditorialReview

- structured review body + 1-5 ratings + status + average_rating property

### ModerationAction

- action log over thesis/comment/user target with reason and reversibility

### UserFeedPreference

- preferred tags, blocked users, minimum rigor threshold

### FeedItem

- cached score tuple per (user, thesis)
- calculate_scores(thesis, user) classmethod

### Sponsorship

- sponsor-sponsoree relation with lifecycle status and optional sponsor rating

### FounderCohort

- named cohort with members, max_size, and active flag

## 6. View/Template Matrix

### Global templates

- templates/index.html (landing + authenticated feed preview)
- templates/registration/login.html
- templates/partials/_home_button.html
- templates/partials/_cookie_banner.html

### Users templates

- templates/users/user_list.html
- templates/users/user_detail.html
- templates/users/my_profile.html
- templates/users/contact_requests.html
- templates/users/sponsorship_requests.html
- templates/users/delete_account_confirm.html
- templates/users/account_deleted.html

### Theses templates

- templates/theses/thesis_list.html
- templates/theses/_thesis_cards.html
- templates/theses/thesis_detail.html
- templates/theses/thesis_review.html
- templates/theses/thesis_form.html

### Feed template

- src/apps/feed/templates/feed/index.html

## 7. HTMX Surface

Implemented HTMX interactions:

- Thesis list search + pagination partial swap.
- Request discrimination via request.htmx (django-htmx middleware).
- Shared HTMX bootstrap loaded from templates/partials/_home_button.html.
- CSRF header propagation for HTMX requests in src/static/js/app_htmx.js.

## 8. Security Baseline

Configured in base/prod settings:

- CSP middleware and explicit directives.
- X-Frame-Options DENY.
- Referrer policy strict-origin-when-cross-origin.
- COOP same-origin.
- Session and CSRF cookie hardening (HttpOnly, SameSite, Secure in prod).
- SSL redirect and HSTS in production.
- CSRF trusted origins configurable via environment in prod.

## 9. Background/Operational Components

- Middleware: UpdateLastActivityMiddleware writes daily activity heartbeat.
- Management command: purge_inactive_users anonymizes inactive accounts.
- CI: .github/workflows/django.yml executes Python 3.12 tests.

## 10. Known Structural Gaps

- tags, moderation, and sponsorship URL modules are placeholders without exposed endpoints.
- CI workflow currently installs requirements.txt while repository uses requirements/*.txt structure.
- feed route redirects to index; app-specific feed template exists but is not mapped through active URL route.

## 11. Fast Navigation Map (By Concern)

- Auth and account lifecycle: apps/users
- Core domain content: apps/theses
- Quality control primitives: apps/tags + apps/moderation
- Ranking and preferences: apps/feed
- Sponsorship cohorts/relations: apps/sponsorship
- Security and middleware: config/settings + users/middleware.py
- Frontend rendering: templates/ and app templates
