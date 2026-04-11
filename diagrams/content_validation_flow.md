# Content Creation and Validation Sequence

```mermaid
sequenceDiagram
    participant U as User
    participant MT as MiniThesis
    participant TA as TagApplication
    participant TV as TagVote
    participant RS as Rigor Score
    participant FI as FeedItem
    participant FA as Feed Algorithm

    Note over U,FA: Thesis Creation & Validation Flow

    U->>MT: Create MiniThesis<br/>(facts, premises, conclusion, limits)
    MT->>TA: Auto-create TagApplication<br/>(pending status)

    loop Community Tagging
        U->>TV: Submit TagVote<br/>(upvote/downvote)
        TV->>TA: Update vote counts
        TA->>TA: Check resolution criteria
    end

    TA->>TA: Resolve tags<br/>(approved/rejected)
    TA->>RS: Calculate rigor score<br/>(0-2 based on tags)

    RS->>FI: Create/update FeedItem<br/>(with calculated score)
    FI->>FA: Apply feed algorithm<br/>(personalized ranking)

    Note over FI: Content appears in user feeds<br/>based on preferences & scores
```