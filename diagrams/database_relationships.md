# Database Relationships (Entity-Relationship Diagram)

```mermaid
erDiagram
    User ||--o{ MiniThesis : authors
    User ||--o{ Comment : writes
    User ||--o{ TagApplication : applies
    User ||--o{ TagVote : votes
    User ||--o| UserFeedPreference : owns
    User ||--o{ FeedItem : receives
    User ||--o{ EditorialReview : reviews
    User ||--o{ ModerationAction : moderates
    User ||--o{ Sponsorship : sponsors
    User ||--o{ Sponsorship : sponsored_by
    User ||--o{ ContactRequest : sends
    User ||--o{ ContactRequest : receives
    User ||--o{ User : sponsors
    User }o--o{ User : contacts

    MiniThesis ||--o{ Comment : has
    MiniThesis ||--o{ Citation : cites_from
    MiniThesis ||--o{ Citation : cites_to
    MiniThesis ||--o{ TagApplication : tagged_with
    MiniThesis ||--o{ FeedItem : appears_in
    MiniThesis ||--o{ EditorialReview : reviewed_by
    MiniThesis ||--o{ ModerationAction : moderated_by
    MiniThesis ||--o{ MiniThesis : follow_up_parent

    Tag ||--o{ TagApplication : used_by
    TagApplication ||--o{ TagVote : voted_on
    UserFeedPreference }o--o{ Tag : preferred_tags
    UserFeedPreference }o--o{ User : blocked_users
    FounderCohort }o--o{ User : members

    User {
        string username
        string email
        string level
        string sponsorship_status
        int tag_accuracy_score
    }

    MiniThesis {
        text thesis
        text facts
        text normative_premises
        text conclusion
        datetime created_at
        bool is_published
    }

    Comment {
        text content
        datetime created_at
    }

    Citation {
        text context
    }

    Tag {
        string name
        text description
    }

    TagApplication {
        text justification
        string status
        int upvotes
        int downvotes
    }

    TagVote {
        bool is_upvote
        datetime created_at
    }

    UserFeedPreference {
        float min_rigor_threshold
    }

    FeedItem {
        float rigor_score
        float engagement_score
        float recency_score
        float total_score
        datetime created_at
    }

    EditorialReview {
        text overall_assessment
        int rigor_rating
        int clarity_rating
        int originality_rating
        string status
    }

    ModerationAction {
        string action_type
        text reason
        bool is_reversible
        datetime created_at
    }

    Sponsorship {
        string status
        int sponsor_rating
        datetime created_at
    }

    FounderCohort {
        string name
        int max_size
        datetime created_at
    }

    ContactRequest {
        string status
        datetime created_at
    }
```