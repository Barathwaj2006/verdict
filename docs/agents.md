# VERDICT Agent Roles & Responsibilities

VERDICT operates an autonomous multi-agent hierarchy where each agent executes specialized tasks using structured Pydantic input/output contracts and clean tool execution.

---

## 1. Lead Agent (`app/agents/lead/agent.py`)
- **Role**: Master Orchestrator & Evaluator
- **Model**: Powered by Gemini 2.5 Flash (`google-genai`).
- **Responsibilities**:
  - Analyzes user decision objectives and constraints.
  - Generates a structured `LeadPlan` containing 1–3 specialized research mission briefs (`ResearchMissionPlan`).
  - Evaluates gathered evidence after each round to determine whether gaps remain or if evidence is sufficient to render a final decision.
  - Produces the final structured `FinalVerdict` (recommendation, confidence score, key findings, risk evaluation, trade-offs).

---

## 2. Specialist Researchers (`app/agents/researchers/specialist.py`)
Executed concurrently by the `ResearchOrchestrator`.

### A. Landscape Researcher
- **Specialization**: Market context, existing solutions, competitors, and industry benchmarks.
- **Mission**: Identifies prior art, competitive offerings, and market standards.

### B. Feasibility Researcher
- **Specialization**: Technical feasibility, implementation complexity, dependencies, and resource constraints.
- **Mission**: Analyzes architectural viability, time-to-build, technical debt, and operational risks.

### C. Opportunity Researcher
- **Specialization**: Value proposition, novelty, user impact, and strategic advantage.
- **Mission**: Evaluates unique differentiation, ROI potential, and strategic alignment.

---

## 3. Skeptic Agent (`app/agents/skeptic/agent.py`)
- **Role**: Adversarial Challenger
- **Responsibilities**:
  - Prioritizes top claims from research using `ClaimPrioritization`.
  - Searches for counter-evidence, weak assumptions, overlooked risks, and contradictions.
  - Generates `SkepticChallenge` objects attached to claims to ensure rigorous critical analysis.
  - **Constraint**: Never marks claims as `VERIFIED`.

---

## 4. Verifier Agent (`app/agents/verifier/agent.py`)
- **Role**: Fact-Checker & Source Auditor
- **Responsibilities**:
  - Audits critical or disputed claims from research and skeptical attack.
  - Conducts independent web searches via `ResearchTool`.
  - Evaluates retrieved external sources against claim statements.
  - Updates claim verification status to `VERIFIED` or `DISPROVED` based strictly on empirical evidence.
