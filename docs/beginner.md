# Beginner Guide

## 1. What Hume Social Is

Hume Social is a structured-discussion platform where people publish mini-theses and the community evaluates quality through tags and reviews.

Unlike conventional social media, content is shaped around argument structure:

- Thesis
- Facts
- Normative premises
- Conclusion
- Declared limits

## 2. Overall Working

At a high level:

1. A user signs up with a sponsor username.
2. Sponsored users can write theses once sponsorship is approved.
3. Other users can apply quality tags and reviewers can publish editorial reviews.
4. The feed ranks content using rigor, engagement, and recency.
5. Users progress by trust and competence (reader -> commentator -> tagger -> editorial reviewer).

## 3. Main Screens

- Home: public landing + authenticated feed preview.
- Theses list: searchable, paginated, HTMX-enhanced updates.
- Thesis detail: full structured argument and highlighted review segments.
- Thesis review tab: tags, editorial reviews, and highlight review form.
- User pages: directory, profile, sponsorship requests, contact requests, GDPR actions.

## 4. Tech Stack (Simple View)

- Backend: Python 3.12, Django 4.2.
- Frontend: Django templates + HTMX + CSS.
- Database: SQLite in local/dev; PostgreSQL intended for production.
- Testing: pytest + Django TestCase.
- Security baseline: CSRF, CSP, secure cookie policies, frame protection, referrer policy.

## 5. How to Run Locally

1. Create and activate virtual environment.
2. Install dependencies from requirements/local.txt.
3. Run migrations in src/.
4. Start server from src/.
5. Run tests from repository root with pytest.

## 6. Core Concepts To Learn Next

- Sponsorship status gates thesis creation/edit.
- Tag applications are not the same as editorial reviews.
- Feed score is a weighted combination, not raw chronology.
- HTMX is used for partial page updates while keeping server-rendered templates.

For implementation details, continue with intermediate.md.
