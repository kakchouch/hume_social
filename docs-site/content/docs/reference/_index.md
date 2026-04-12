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

- [Users App]({{< relref "/docs/reference/users.md" >}})
- [Theses App]({{< relref "/docs/reference/theses.md" >}})
- [Tags App]({{< relref "/docs/reference/tags.md" >}})
- [Moderation App]({{< relref "/docs/reference/moderation.md" >}})
- [Feed App]({{< relref "/docs/reference/feed.md" >}})
- [Sponsorship App]({{< relref "/docs/reference/sponsorship.md" >}})

## Template Reference

- [Template Catalog and Context Contracts]({{< relref "/docs/reference/templates.md" >}})

## Cross-App Navigation

- Entry routes and app boundaries: [Expert Reference]({{< relref "/docs/expert.md" >}})
- High-level onboarding: [Beginner Guide]({{< relref "/docs/beginner.md" >}})
- Runtime flow and HTMX patterns: [Intermediate Guide]({{< relref "/docs/intermediate.md" >}})

## Linking Rules Used In This Reference

Each object section includes:

- Source link to the exact Python or HTML file.
- Parameter/field documentation.
- Related object links across app docs.
- Calling/called-by links where relevant.
