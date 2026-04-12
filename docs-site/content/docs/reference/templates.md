---
title: "Template Reference"
---

# Template Catalog and Context Contracts

This document maps each rendered template to the view that calls it and the expected context keys.

## Human-Readable Summary

- Aim of the objects: document UI templates as runtime objects with clear contracts.
- Broader role: templates are the presentation boundary between backend domain logic and user-visible workflows.
- Specific role: each template section describes which view calls it and which context keys it expects so contributors can safely evolve view/template pairs.
- Inputs and outputs:
	- Inputs: context dictionaries from views, auth/session state, HTMX request shape (for fragment templates).
	- Outputs: rendered HTML pages/fragments, form surfaces, action links and buttons that trigger subsequent endpoints.

## Global Templates

### `templates/index.html`

- Called by: [users.landing_page]({{< relref "/docs/reference/users.md" >}}#landing_pagerequest)
- Context keys: `signup_form`, `feed_items`, `min_rigor_threshold`

### `templates/registration/login.html`

- Called by: Django `LoginView` configured in root URLs
- Context keys: Django auth defaults (`form`, `next`, `site`, etc.)

### `templates/partials/_home_button.html`

- Included by: most pages as shared nav/home control

### `templates/partials/_cookie_banner.html`

- Included by: most pages
- Posts to: [users.cookie_consent]({{< relref "/docs/reference/users.md" >}}#cookie_consentrequest)

## Users Templates

### `templates/users/user_list.html`

- Called by: [users.user_list]({{< relref "/docs/reference/users.md" >}}#user_listrequest)
- Context keys: `users`, `search_query`

### `templates/users/user_detail.html`

- Called by: [users.user_detail]({{< relref "/docs/reference/users.md" >}}#user_detailrequest-pk)
- Context keys: `profile_user`, `sponsored_users`, `contacts`, `contact_state`, `incoming_request`

### `templates/users/my_profile.html`

- Called by: [users.my_profile]({{< relref "/docs/reference/users.md" >}}#my_profilerequest)
- Context keys: `form`, `profile_user`, `sponsored_users`, `contacts`

### `templates/users/contact_requests.html`

- Called by: [users.contact_requests]({{< relref "/docs/reference/users.md" >}}#contact_requestsrequest)
- Context keys: `incoming_requests`, `outgoing_requests`

### `templates/users/sponsorship_requests.html`

- Called by: [users.sponsorship_requests]({{< relref "/docs/reference/users.md" >}}#sponsorship_requestsrequest)
- Context keys: `pending_users`

### `templates/users/delete_account_confirm.html`

- Called by: [users.delete_account]({{< relref "/docs/reference/users.md" >}}#delete_accountrequest)
- Context keys: `form`

### `templates/users/account_deleted.html`

- Called by: [users.account_deleted]({{< relref "/docs/reference/users.md" >}}#account_deletedrequest)
- Context keys: none required

## Theses Templates

### `templates/theses/thesis_list.html`

- Called by: [theses.thesis_list]({{< relref "/docs/reference/theses.md" >}}#thesis_listrequest)
- Context keys: `page_obj`, `search_query`, `can_write_theses`
- Includes HTMX partial: `templates/theses/_thesis_cards.html`

### `templates/theses/_thesis_cards.html`

- Called by: `thesis_list` HTMX response and full-page include
- Context keys: `page_obj`

### `templates/theses/thesis_detail.html`

- Called by: [theses.thesis_detail]({{< relref "/docs/reference/theses.md" >}}#thesis_detailrequest-pk)
- Context keys: `thesis`, `follow_up_theses`, `review_count`, `tag_count`, `highlighted_sections`

### `templates/theses/thesis_review.html`

- Called by: [theses.thesis_review]({{< relref "/docs/reference/theses.md" >}}#thesis_reviewrequest-pk)
- Context keys: `thesis`, `tag_applications`, `editorial_reviews`, `highlight_reviews`, `review_highlight_form`, `can_add_highlight_review`

### `templates/theses/thesis_form.html`

- Called by: [theses.thesis_create]({{< relref "/docs/reference/theses.md" >}}#thesis_createrequest-parent_pknone), [theses.thesis_edit]({{< relref "/docs/reference/theses.md" >}}#thesis_editrequest-pk)
- Context keys: `form`, `title`, `parent_thesis` (create only)

## Feed Template

### `src/apps/feed/templates/feed/index.html`

- Legacy template; active `/feed/` route currently redirects to index
- Related view: [FeedHomeView]({{< relref "/docs/reference/feed.md" >}}#feedhomeview)

## Related Documentation

- [Users App]({{< relref "/docs/reference/users.md" >}})
- [Theses App]({{< relref "/docs/reference/theses.md" >}})
- [Expert overview]({{< relref "/docs/expert.md" >}})
