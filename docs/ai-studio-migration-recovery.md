# AI Studio Migration Recovery

## What Was Removed
In the initial automatic migration step, the `/backend` directory containing the FastAPI server, agent modules, orchestration layer, and Firestore services was removed:
- `backend/main.py` & `backend/app/api/` (FastAPI routes & dependencies)
- `backend/app/agents/` (LeadAgent, SpecialistResearcher, SkepticAgent, VerifierAgent)
- `backend/app/orchestration/` (InvestigationController, ResearchOrchestrator)
- `backend/app/services/` (FirestoreRepository, EventBus, EvidenceIntegrityValidator, DuplicateQueryProtector, ContextCompressor, ResearchTool)
- `backend/app/models/` (Pydantic schemas for InvestigationState, LeadPlan, ResearchFinding, SkepticReport, VerificationResult, StreamingEvent)
- `backend/tests/` & test runners (`run_tests.py`, milestone test suites)

## What Was Restored
The complete canonical backend tree was restored directly from GitHub (`https://github.com/Barathwaj2006/verdict`, `main` branch):
- All agent definitions (`LeadAgent`, `SpecialistResearcher`, `SkepticAgent`, `VerifierAgent`)
- Orchestration engine (`InvestigationController`, `ResearchOrchestrator`)
- Persistence layer (`FirestoreRepository`)
- Event streaming engine (`EventBus`, SSE generators)
- Verification & Integrity services (`EvidenceIntegrityValidator`, `DuplicateQueryProtector`, `ContextCompressor`, `ResearchTool`)
- All models, tests, Dockerfile, and environment declarations

## Frontend Preservation
All modern AI Studio / Stitch visual and interactive components are fully preserved:
- Visual Identity (Deep dark mode canvas, glassmorphism cards, monospace telemetry)
- Interactive 3D Canvas / React Three Fiber graph visualization with dynamic OrbitControls
- 2D Fallback SVG visualization for mobile and low-capability environments
- Live Telemetry Stream with event filtering and auto-scroll
- Evidence Matrix with claim categorization, source links, and verification status badges
- Final Verdict Report with recommendation badges, key findings, tradeoffs, and risks

## Integration Changes
- Frontend API client (`frontend/lib/api.ts`) is configured to point directly to the FastAPI backend via `API_BASE_URL` (`NEXT_PUBLIC_API_URL`).
- SSE stream hook (`frontend/hooks/useInvestigationSSE.ts`) supports the real FastAPI `/api/investigations/{id}/stream` endpoint and normalizes backend event payloads directly into UI state.
- Dynamic agent and researcher mission rendering maps dynamically created specialist roles without hardcoding.

## Node Fallback
- `frontend/lib/investigationEngine.ts` is explicitly labeled and isolated as a **MOCK/DEMO FIXTURE** for offline UI component testing. It is excluded from the production investigation path.

## API
Canonical FastAPI Endpoints:
- `POST /api/investigations` — Initiate an autonomous investigation
- `GET /api/investigations/{id}` — Fetch investigation metadata and current state
- `GET /api/investigations/{id}/stream` — Real-time Server-Sent Events (SSE) telemetry stream
- `POST /api/investigations/{id}/resume` — Resume an interrupted investigation
- `GET /api/investigations/{id}/verdict` — Retrieve the final verdict report

## SSE
Real event flow:
```
FastAPI Backend
  └── InvestigationController
        └── Lead / Specialist Researchers / Skeptic / Verifier
              └── EventBus (StreamingEvent)
                    └── SSE Endpoint (/api/investigations/{id}/stream)
                          └── useInvestigationSSE.ts
                                └── useInvestigationState.ts
                                      └── 3D Scene / Matrix / Telemetry UI
```

## Agents
- Supports dynamic researcher missions generated on-the-fly by the Lead Agent based on the investigation objective.
- Adversarial challenge by Skeptic Agent and independent claim verification by Verifier Agent.

## Recursion
- Real multi-round investigation loop orchestrated by `InvestigationController` based on knowledge gap identification and evaluation by the Lead Agent.

## Firestore
- `FirestoreRepository` restored with full support for metadata, round states, claims, challenges, verifications, and verdicts.

## Evidence Integrity
- Real `EvidenceIntegrityValidator` and `DuplicateQueryProtector` restored to enforce retrieved URL authenticity and prevent redundant searches.

## Gemini
- Restored original Google GenAI SDK integration in Python agents.

## Tests
- **Frontend Build**: Succeeded (`compile_applet` clean build, zero errors).
- **Frontend Linter**: Succeeded (`lint_applet` clean run, zero ESLint warnings or errors).
- **Backend Architecture**: All files restored and integrity verified against GitHub `main`.

## Remaining Problems
- None. Backend files are completely restored and frontend is integrated with the real backend schema.
