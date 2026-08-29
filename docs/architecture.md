# VERDICT System Architecture

## Overview
VERDICT is an autonomous decision-research engine designed to evaluate complex objectives, gather empirical evidence, challenge key claims through skeptical analysis, independently verify disputed evidence, and converge recursively on a final verdict.

Phase 1 (M0–M9 + M5.5) represents the complete, fully audited, and frozen backend orchestration engine and baseline frontend stream consumer (Audit Score: 95/100, Freeze Commit: `619061f`).

---

## High-Level System Architecture

```
                                  +-----------------------+
                                  |     Next.js UI        |
                                  |  (React, TypeScript)  |
                                  +-----------+-----------+
                                              |
                                      HTTP / SSE Stream
                                              |
                                              v
                                  +-----------------------+
                                  |    FastAPI Server     |
                                  |     (main.py / REST)  |
                                  +-----------+-----------+
                                              |
                                              v
                               +-----------------------------+
                               |   InvestigationController   |
                               +--------------+--------------+
                                              |
                                              v
                              +-------------------------------+
                              |          Lead Agent           |
                              | (Gemini 2.5 Flash / Dynamic)  |
                              +---------------+---------------+
                                              |
             +--------------------------------+--------------------------------+
             |                                |                                |
             v                                v                                v
+--------------------------+     +--------------------------+     +--------------------------+
|   Landscape Researcher   |     |  Feasibility Researcher  |     |  Opportunity Researcher  |
|  (DuckDuckGo Search)     |     |  (DuckDuckGo Search)     |     |  (DuckDuckGo Search)     |
+------------+-------------+     +------------+-------------+     +------------+-------------+
             |                                |                                |
             +--------------------------------+--------------------------------+
                                              |
                                              v
                                 +--------------------------+
                                 |   Evidence Integrity     |
                                 |  Validator (M5.5)        |
                                 +------------+-------------+
                                              |
                                              v
                                 +--------------------------+
                                 |      Skeptic Agent       |
                                 | (Claims Attack / DDG)    |
                                 +------------+-------------+
                                              |
                                              v
                                 +--------------------------+
                                 |     Verifier Agent       |
                                 | (Fact Checker / DDG)     |
                                 +------------+-------------+
                                              |
                                              v
                                 +--------------------------+
                                 |  Firestore Persistence   |
                                 |  (Round-by-Round State)  |
                                 +--------------------------+
```

---

## Core Components

### 1. Investigation Controller (`app/orchestration/investigation_controller.py`)
- Manages the multi-round execution loop (up to `MAX_ROUNDS = 3`).
- Coordinates state updates across rounds and interacts directly with `FirestoreRepository`.
- Publishes execution steps to `EventBus` for Real-time SSE streaming.

### 2. Lead Agent (`app/agents/lead/agent.py`)
- Powered by `google-genai` (Gemini 2.5 Flash).
- Analyzes user objectives and constraints.
- Dynamically creates specialized research missions (Landscape, Feasibility, Opportunity).
- Evaluates round evidence and determines whether a gap exists or if a final verdict can be issued.

### 3. Research Orchestrator & Specialist Researchers (`app/orchestration/research_orchestrator.py`, `app/agents/researchers/`)
- Executes research missions concurrently (`asyncio.gather`).
- Leverages `DuckDuckGoSearchProvider` (`duckduckgo-search`) for web research.
- Formulates claims backed by empirical evidence sources.

### 4. Evidence Integrity Validator (`app/services/evidence_integrity.py`)
- M5.5 Mechanism: Prevents hallucinated citations and unverified URLs from entering state.
- Strips invalid or fake links, preserves valid external sources, and flags model internal knowledge appropriately.

### 5. Skeptic Agent (`app/agents/skeptic/agent.py`)
- Adversarial agent that prioritizes top claims and searches for counter-evidence, hidden risks, and false assumptions.
- Attacks claims to weaken or invalidate flawed findings before final evaluation.

### 6. Verifier Agent (`app/agents/verifier/agent.py`)
- Independent fact-checker that verifies disputed claims against external ground-truth search results.
- Transitions claims from `UNVERIFIED` to `VERIFIED` or `DISPROVED`.

### 7. Event Bus & Real-Time SSE (`app/services/event_bus.py`, `app/api/routes.py`)
- Broadcasts structured, non-CoT execution events to frontend clients via Server-Sent Events (`/api/investigations/{id}/events`).
