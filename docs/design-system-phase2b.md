# VERDICT — Phase 2B: Premium UI/UX Design System & Specification

## Executive Overview

**VERDICT** is an autonomous multi-agent decision-research engine. Phase 1 (M0–M9 + M5.5) provided a robust, frozen backend engine with dynamic Lead orchestration, specialist researchers, anti-hallucination evidence validation, Skeptic attacks, independent Verifier audit, and Firestore persistence.

Phase 2B establishes the visual language, spatial 3D direction, interaction architecture, and component system for the frontend. The design system transforms VERDICT into an award-grade **AI Research Command Center**, combining chatbot-first conversational simplicity with cinematic, real-time multi-agent investigation visualization.

---

## 🎨 1. Visual Identity & Performance-First Principles

### Core Principles
1. **Performance Outranks Visual Complexity**: The 3D layer (`@react-three/fiber`) is ambient and purposeful, never a heavy always-running scene. SVG/2D canvas fallback is primary for low-power or mobile environments.
2. **Chatbot-First Surface**: The conversational input and telemetry stream form the primary user interface. 3D visualization supports investigation clarity without becoming a distraction.
3. **5–10 Second Verdict Readability**: Final verdicts present an authoritative executive briefing readable at a glance (Recommendation, Confidence Gauge, Top Findings) with optional drill-down.
4. **Dark-First Command Center**: Obsidian space background (`#07080C`) with subtle radiant gradients and glassmorphic surface overlays (`backdrop-blur-xl`).

### Color Palette

| Token | Hex / HSL | Usage |
| :--- | :--- | :--- |
| `--bg-obsidian` | `#07080C` | Root page background |
| `--bg-card` | `rgba(15, 18, 28, 0.75)` | Glassmorphic cards & panels |
| `--border-subtle` | `rgba(255, 255, 255, 0.08)` | Standard component borders |
| `--border-luminous` | `rgba(99, 102, 241, 0.3)` | Focused / active state borders |
| `--agent-lead` | `#818CF8` / Indigo-400 | Lead Orchestrator accent |
| `--agent-landscape` | `#38BDF8` / Sky-400 | Landscape Specialist accent |
| `--agent-feasibility` | `#F59E0B` / Amber-500 | Feasibility Specialist accent |
| `--agent-opportunity` | `#10B981` / Emerald-500 | Opportunity Specialist accent |
| `--agent-skeptic` | `#F43F5E` / Rose-500 | Skeptic Agent attack accent |
| `--agent-verifier` | `#10B981` / Emerald-400 | Verifier Agent audit accent |
| `--status-supports` | `#10B981` | Supporting evidence badge |
| `--status-contradicts` | `#F43F5E` | Contradicting evidence badge |
| `--status-qualifies` | `#F59E0B` | Qualifying evidence badge |
| `--status-unverified` | `#6B7280` | Unverified claim badge |

---

## 🖥 2. Core Experience States & Views

### State 1: Landing & Investigation Start (Chatbot-First)
- **Central Element**: Hero prompt box with instant focus, multi-line support, and natural language example chips:
  - *"Find me the strongest project idea for this hackathon. I have 3 days and I’m working alone."*
  - *"Should we migrate our backend service from Node.js to Python/FastAPI for ML tasks?"*
- **Visual Background**: Subtle 3D ambient particle cloud reacting gently to mouse hover.

### State 2: Investigation Workspace & Telemetry Stream
- **Header Bar**: Objective summary pill, live status badge (`INITIALIZING`, `RESEARCHING`, `SKEPTIC_ATTACK`, `VERIFYING`, `EVALUATING`, `COMPLETED`), current round indicator, and total elapsed execution time.
- **Left Panel (Chronological Stream)**: Real-time execution log consuming SSE events (`ROUND_START`, `LEAD_PLAN_CREATED`, `RESEARCH_COMPLETED`, etc.) with animated pulse indicators.
- **Center Canvas (Interactive Agent & Evidence Graph)**: Dynamic agent nodes and active research missions.
- **Right Panel (Inspected Claim & Evidence Drawer)**: Expands when any node or claim card is selected to display raw web citations and skeptical attacks.

---

## 🤖 3. Dynamic Agent Visualization & Branching Graph

- Supports dynamically generated specialist roles created by Lead Agent `ResearchMissionPlan`.
- **Node Hierarchy**:
  ```
                        [ LEAD AGENT ]
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
  [ Specialist 1 ]     [ Specialist 2 ]     [ Specialist N ]
         │                    │                    │
         └────────────────────┼────────────────────┘
                              ▼
                      [ SKEPTIC AGENT ]
                              │
                              ▼
                     [ VERIFIER AGENT ]
                              │
                              ▼
                     [ EVALUATION / GAP ]
                              │
              (If gap exists: Branch Round 2)
  ```
- **Visual Branching**: Historical rounds remain visible in semi-transparent state (`opacity: 0.5`), while new rounds branch visually from knowledge gap nodes.

---

## 🛡 4. Evidence Interface & Claim Matrix

Each evidence card presents:
1. **Claim Statement**: Highlighted assertion.
2. **Verification Badge**: `VERIFIED` (Green), `UNVERIFIED` (Gray), or `DISPROVED` (Red).
3. **Evidence Relationship Badge**: `SUPPORTS`, `CONTRADICTS`, `QUALIFIES`, `IRRELEVANT`.
4. **Source Quality & Domain**: Validated domain (e.g. `devpost.com`) and direct link.
5. **Skeptic Challenge Callout**: Expandable accordion detailing counter-arguments raised by Skeptic Agent.
6. **Verifier Audit Detail**: Specific search queries and disproof/verification logic.

---

## 🏆 5. Authoritative Final Verdict Presentation (5–10 Second Executive Readability)

1. **Headline Conclusion**: Recommendation (`PROCEED`, `PIVOT`, or `ABORT`) with high-contrast badge.
2. **Confidence Metric**: Large radial confidence gauge / percentage readout.
3. **Top Verified Findings**: Concise bulleted list of claims that survived Skeptic attack and Verifier audit.
4. **Critical Trade-Offs & Risks**: High-visibility warning box outlining identified technical debt or risks.
5. **Audit Trail Telemetry**: Claims analyzed, sources verified, Skeptic attacks executed, and total rounds required.
