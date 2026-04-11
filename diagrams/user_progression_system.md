# User Progression and Permission System

```mermaid
stateDiagram-v2
    [*] --> Reader: Account Creation

    Reader --> Commentator: Level Up
    Commentator --> Tagger: Level Up
    Tagger --> Reviewer: Level Up

    Reader: Can read content
    Commentator: Can read + comment
    Tagger: Can read + comment + tag
    Reviewer: Can read + comment + tag + review

    note right of Reader
        Basic user level
        Limited permissions
    end note

    note right of Commentator
        Can engage in discussions
        Build reputation through comments
    end note

    note right of Tagger
        Can participate in content validation
        Tag accuracy affects reputation
    end note

    note right of Reviewer
        Editorial oversight
        Can moderate content
    end note

    Reviewer --> [*]: Account management
```