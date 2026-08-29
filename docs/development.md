# Developer Guide & Phase 1 Freeze Notice

## Phase 1 Frozen State Notice
- **Milestones**: Phase 1 (M0–M9 + M5.5) application logic, agent implementations, API routes, and Firestore persistence layer are 100% complete and **FROZEN**.
- **Audit Score**: 95/100
- **Freeze Commit**: `619061f`
- **Backend Test Suite**: 35 passing unit & integration tests.
- **Rule for Phase 2**: Do NOT modify Phase 1 application code, agent behaviors, or backend routes.

---

## Local Development Setup

### 1. Prerequisites
- Python 3.12+
- Node.js 18+ / npm
- Google Gemini API Key

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run backend test suite
PYTHONPATH=. pytest tests -v

# Start FastAPI dev server
uvicorn main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start Next.js dev server
npm run dev
```

---

## Testing Framework

Backend tests are located under `backend/tests/`.

Run tests with:
```bash
PYTHONPATH=backend pytest backend/tests -v
```

### Test Suites Included:
- `test_api.py`: FastAPI endpoints and HTTP responses.
- `test_controller.py`: `InvestigationController` loop, round progression, and stopping conditions.
- `test_evidence_acquisition.py`: Specialist researchers and DuckDuckGo search integration.
- `test_firestore_repository.py`: Firestore persistence state loading/saving.
- `test_m55.py`: Evidence integrity validator, duplicate query protector, event bus, and context compression.
- `test_research_orchestrator.py`: Parallel research execution and isolation.
- `test_skeptic.py`: Skeptic attack logic, claim prioritization, and search failure handling.
- `test_verifier.py`: Independent claim verification and disproof handling.
