# User Progression and Permission System

```mermaid
stateDiagram-v2
    [*] --> Reader: Account created

    state SponsorshipGate {
        [*] --> Pending
        Pending --> Approved: Sponsor approves
        Pending --> Rejected: Sponsor rejects
        Rejected --> Pending: New sponsor flow
    }

    Reader --> Commentator: Level grant
    Commentator --> Tagger: Level grant
    Tagger --> EditorialReviewer: Level grant

    Reader: Read content
    Commentator: Read + comment
    Tagger: Read + comment + tag
    EditorialReviewer: Read + comment + tag + review

    note right of SponsorshipGate
        thesis_create and thesis_edit require
        sponsorship_status != pending
    end note

    note right of Tagger
        tag_accuracy_score is clamped between 0 and 2
    end note

    EditorialReviewer --> [*]: Account deactivated or deleted
```