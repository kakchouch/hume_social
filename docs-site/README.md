# Hugo Documentation Site

This folder contains a Hugo documentation site for Hume Social using the Risotto theme.

## What is included

- Homepage aligned with the main project README messaging.
- Documentation pages under `/docs/`.
- Object-level references under `/docs/reference/`.
- Diagram pages under `/diagrams/`.
- Internal links rewritten to site routes (not repository paths).

## Run locally

From this folder:

```bash
hugo server -D
```

Then open:

- http://localhost:1313/

## Build static output

```bash
hugo
```

The generated site will be in `public/`.
