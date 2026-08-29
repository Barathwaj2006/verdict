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
- Google Cloud CLI (`gcloud`)

### 2. Local Google Cloud Authentication
To run the VERDICT backend locally, you must use Application Default Credentials (ADC). Do NOT create or commit service-account JSON keys in this repository.

1. **Install Google Cloud CLI** from the official Google documentation.
2. **Run `gcloud init`** to select the correct Google Cloud project.
3. **Run `gcloud auth application-default login`**. This securely generates local ADC credentials outside of the repository.
4. **Configure Environment Variables**: Copy `.env.example` to `.env` in the root and provide your `GEMINI_API_KEY` and `GOOGLE_CLOUD_PROJECT`.
5. **Start the Backend**: `uvicorn main:app --host 127.0.0.1 --port 8000`.

*Note: ADC credentials are automatically stored in your user profile outside the repository and must never be committed.*

### 3. Backend Setup
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
