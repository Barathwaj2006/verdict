# Evidence Integrity & Anti-Hallucination Mechanisms

VERDICT implements a multi-layered evidence integrity architecture to guarantee that decision research remains grounded, verifiable, and free from artificial LLM hallucinations.

---

## Key Anti-Hallucination Controls

### 1. Citation Validation & URL Verification (`EvidenceIntegrityValidator`)
- **Module**: `app/services/evidence_integrity.py` (M5.5)
- **Operation**:
  - Validates every URL returned in agent evidence payloads against actual retrieved search results.
  - Strips fake, hallucinated, or malformed URLs.
  - Retains source snippets only when backed by genuine domain sources.
  - Differentiates between verified web citations and internal LLM baseline knowledge.

### 2. Duplicate Query Protection (`DuplicateQueryProtector`)
- **Module**: `app/services/evidence_integrity.py`
- **Operation**:
  - Tracks search queries across rounds to prevent repetitive or looping queries.
  - Automatically filters duplicate queries to maximize search efficiency and evidence breadth.

### 3. Context Compression (`ContextCompressor`)
- **Module**: `app/services/evidence_integrity.py`
- **Operation**:
  - Compresses prior round research, claim states, and skeptical counterarguments into dense context summaries.
  - Prevents prompt window dilution while preserving critical entities and verified claims across long research loops.

### 4. Grounding & Disproof Verification
- **Status Pipeline**: Claims start in `UNVERIFIED` state.
- **Verification Rule**: Claims can only transition to `VERIFIED` if backed by validated external sources checked by the Verifier Agent.
- **Disproof Rule**: Claims contradicted by empirical counter-evidence are set to `DISPROVED`, preventing false assertions from influencing the final verdict.
