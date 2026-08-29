# VERDICT Architecture

VERDICT is structured as a decoupled backend orchestration engine exposing real-time state via FastAPI.

## Data Flow

```mermaid
graph TD
    User([Frontend / User]) -->|POST /api/investigations| API[FastAPI Entrypoint]
    API --> Controller[InvestigationController]
    
    subgraph Autonomous Engine
        Controller --> Lead[Lead Agent]
        Lead -->|Creates| Missions[Research Missions]
        Missions --> Specialist[Specialist Researchers]
        Specialist -->|Fetches| Tools[External Sources / DDG]
        Specialist --> Skeptic[Skeptic Agent]
        Skeptic -->|Generates Challenges| Verifier[Verifier Agent]
        Verifier --> Lead
    end

    Controller -.->|Checkpoints| Firestore[(Google Cloud Firestore)]
    
    subgraph Live Streaming
        Controller --> Bus[EventBus]
        Specialist --> Bus
        Skeptic --> Bus
        Verifier --> Bus
        Bus -->|SSE| Stream[FastAPI /stream endpoint]
        Stream -->|Real-time Events| User
    end
```

## Key Components
- **API routes**: Manages background execution and SSE streams.
- **InvestigationController**: Executes the core recursive algorithm.
- **EventBus**: Asynchronous dispatcher. Allows arbitrary HTTP endpoints to subscribe dynamically.
- **FirestoreRepository**: Canonical persistent store. Ensures complete failure recovery via M6 checkpointing rules.
