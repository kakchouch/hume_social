---
title: "Reference Map"
---

# Technical Reference Map

This reference is object-level documentation for apps, classes, parameters, and templates.

## Human-Readable Summary

- Aim of the objects: describe what each app object does in plain language (models, views, forms, templates, routes).
- Broader role: explain how each object supports the platform lifecycle (signup, thesis publishing, review, moderation, feed quality).
- Specific role: document each object's direct responsibility and where it sits in request/data flows.
- Inputs and outputs: make explicit what each object receives (request data, model fields, form values, context keys) and what it returns (DB rows, rendered pages, redirects, JSON).

## App References

- [Users App](/docs/reference/users/)
- [Theses App](/docs/reference/theses/)
- [Tags App](/docs/reference/tags/)
- [Moderation App](/docs/reference/moderation/)
- [Feed App](/docs/reference/feed/)
- [Sponsorship App](/docs/reference/sponsorship/)

## Template Reference

- [Template Catalog and Context Contracts](/docs/reference/templates/)

## Cross-App Navigation

- Entry routes and app boundaries: [Expert Reference](/docs/expert/)
- High-level onboarding: [Beginner Guide](/docs/beginner/)
- Runtime flow and HTMX patterns: [Intermediate Guide](/docs/intermediate/)

## Linking Rules Used In This Reference

Each object section includes:

- Source link to the exact Python or HTML file.
- Parameter/field documentation.
- Related object links across app docs.
- Calling/called-by links where relevant.
