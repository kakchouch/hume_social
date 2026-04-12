# Content Creation and Validation Sequence

```mermaid
sequenceDiagram
    participant Browser
    participant Middleware as Django Middleware Stack
    participant UserView as users.landing_page
    participant ThesisCreate as theses.thesis_create
    participant ThesisList as theses.thesis_list
    participant MiniThesis as MiniThesis
    participant TagApplication as TagApplication
    participant TagVote as TagVote
    participant EditorialReview as EditorialReview
    participant FeedScore as FeedItem.calculate_scores

    Note over Browser,FeedScore: Live runtime flow with HTMX + security middleware

    Browser->>Middleware: GET / (or /theses/)
    Middleware->>UserView: Route dispatch after security, session, CSRF, auth, HTMX middleware
    UserView-->>Browser: Landing page (or authenticated feed preview)

    Browser->>Middleware: POST /theses/create/
    Middleware->>ThesisCreate: Authenticated request
    ThesisCreate->>ThesisCreate: can_write_theses() sponsorship gate
    ThesisCreate->>MiniThesis: Persist thesis if valid
    ThesisCreate-->>Browser: Redirect to thesis detail

    Browser->>Middleware: GET /theses/?q=... (hx-request optional)
    Middleware->>ThesisList: request.htmx available
    ThesisList->>MiniThesis: Query + rank by rigor_score
    ThesisList-->>Browser: Full page or _thesis_cards fragment

    Browser->>TagApplication: Apply quality tag
    Browser->>TagVote: Vote on application validity
    TagVote->>TagApplication: Update vote counters

    Browser->>EditorialReview: Publish editorial review

    Browser->>Middleware: Open feed/landing as authenticated user
    Middleware->>UserView: Compute feed candidates
    UserView->>FeedScore: calculate_scores(thesis, user)
    FeedScore-->>UserView: rigor + engagement + recency + total
    UserView-->>Browser: Ranked feed items
```