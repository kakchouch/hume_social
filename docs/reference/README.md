# Technical Reference Map

This reference is object-level documentation for apps, classes, parameters, and templates.

## Human-Readable Summary

- Aim of the objects: describe what each app object does in plain language (models, views, forms, templates, routes).
- Broader role: explain how each object supports the platform lifecycle (signup, thesis publishing, review, moderation, feed quality).
- Specific role: document each object's direct responsibility and where it sits in request/data flows.
- Inputs and outputs: make explicit what each object receives (request data, model fields, form values, context keys) and what it returns (DB rows, rendered pages, redirects, JSON).

## App References

- [Users App](users.md)
- [Theses App](theses.md)
- [Tags App](tags.md)
- [Moderation App](moderation.md)
- [Feed App](feed.md)
- [Sponsorship App](sponsorship.md)

## Template Reference

- [Template Catalog and Context Contracts](templates.md)

## Cross-App Navigation

- Entry routes and app boundaries: [../expert.md](../expert.md)
- High-level onboarding: [../beginner.md](../beginner.md)
- Runtime flow and HTMX patterns: [../intermediate.md](../intermediate.md)

## Linking Rules Used In This Reference

Each object section includes:

- Source link to the exact Python or HTML file.
- Parameter/field documentation.
- Related object links across app docs.
- Calling/called-by links where relevant.
