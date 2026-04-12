---
title: "Intermediate Guide"
---

# Intermediate Guide

## 1. Architecture In Practice

The project is a Django monolith with domain apps under src/apps.

- users: identity, profile, sponsorship status, contact graph, GDPR workflows.
- theses: authoring, listing, detail/review display, follow-ups.
- tags: community tag taxonomy, tag applications, votes.
- moderation: editorial reviews and moderation actions.
- feed: preference model + score calculation + legacy feed route.
- sponsorship: sponsorship and founder cohort models.

## 2. Request Lifecycle

A typical request goes through:

1. Django security middleware.
2. CSP middleware.
3. Session middleware.
4. HTMX middleware (adds request.htmx context).
5. CSRF/auth/message middleware.
6. UpdateLastActivityMiddleware (daily touch for authenticated users).
7. Target app view.
8. Template render (full page or HTMX fragment).

## 3. HTMX Integration Pattern

Current pattern is implemented in thesis list:

- Full GET returns templates/theses/thesis_list.html.
- HTMX GET returns templates/theses/_thesis_cards.html.
- Search and pagination use hx-get/hx-target/hx-push-url.
- Shared partial loads self-hosted HTMX and app_htmx.js for CSRF header injection.

This pattern can be reused in other list/detail interfaces.

## 4. Content Quality Pipeline

1. Author publishes MiniThesis.
2. Community applies TagApplication entries and votes with TagVote.
3. Editorial reviewers publish EditorialReview items.
4. Optional ThesisReviewHighlight links selected text to a tag + reviewer note.
5. FeedItem.calculate_scores combines:
   - rigor score from thesis tags
   - engagement score from follow-up/citation/review signals
   - recency decay

## 5. Sponsorship and Progression

- Signup requires sponsor username.
- New account starts with sponsorship_status = pending.
- Users cannot create or edit theses while pending.
- Sponsor decides via sponsorship requests UI.
- User level methods (can_comment/can_tag/can_review) enforce capability checks in views.

## 6. Privacy and GDPR Flow

Available user actions:

- Download personal data as JSON.
- Delete account via password confirmation.
- Account deletion anonymizes personal fields and disables login.
- Management command purge_inactive_users anonymizes stale accounts by policy.

## 7. Testing Strategy

- Model tests validate score bounds, uniqueness constraints, and computed properties.
- View tests cover authorization, redirects, sponsorship constraints, and rendered pages.
- HTMX tests verify fragment-only responses and script presence.
- Feed tests verify ordering and preference threshold behavior.

## 8. CI and Deployment Notes

- GitHub Actions runs Django test command on Python 3.12.
- Production settings enforce SSL redirect, secure cookies, HSTS, and trusted CSRF origins.
- CSP and frame protections are defined centrally in base settings.

For complete inventories and field-level references, see expert.md.
