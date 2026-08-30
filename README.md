# VERDICT: Autonomous Decision-Research Engine

## 🌍 The Problem
Generative AI excels at answering questions quickly, but real-world decision-making requires investigation. Whether a team is evaluating an architecture migration, a legal claim, or a competitive threat, standard LLMs often hallucinate, summarize poorly, or stop at surface-level answers. 

## 💡 The Solution
VERDICT is an autonomous, multi-agent investigation system that mimics a real-world research team. It doesn't just answer; it plans, researches, aggressively challenges its own findings, independently verifies sources, and recursively hunts for the truth before issuing an executive decision.

---

## 🚀 Google Technologies
VERDICT is built exclusively on a modern Google Cloud stack:
- **Google Gemini:** Powered by `gemini-3.7-flash` for high-speed, complex reasoning.
- **Google GenAI SDK:** Uses native structured outputs to deterministically orchestrate agents without fragile prompt-engineering.
- **Google Cloud Firestore:** Provides durable, round-by-round persistence of evidence matrices and agent states.
- **Google Cloud Run:** Fully containerized backend designed for serverless execution.

---

## 🤖 Agentic Architecture & Recursion

VERDICT uses a dynamic hierarchy of specialized agents:

1. **Lead Agent:** Evaluates the problem, creates dynamic research missions, and acts as the final judge.
2. **Specialist Researchers:** Spawned concurrently to scrape the web and extract evidence.
3. **Skeptic Agent:** Adversarially challenges claims, looking for logical flaws or unsupported statements.
4. **Verifier Agent:** Runs independent secondary searches to confirm or refute the Skeptic's challenges.

**Recursion:** If the Lead Agent identifies a "Knowledge Gap" in the verified evidence, it autonomously loops back and spawns a new round of targeted research. The investigation continues until an evidence threshold is met or the `MAX_ROUNDS` limit is reached.

---

## 🛡 Evidence Integrity & Anti-Hallucination

- **Citation Validation**: Strips hallucinated or unreachable URLs from research evidence before state storage using Python-level validation.
- **Duplicate Query Protector**: Prevents looping or repetitive searches across research rounds.
- **Verification Thresholds**: Claims default to `UNVERIFIED` and only transition to `VERIFIED` when verified by independent web sources.

---

## 📂 Project Structure

- `backend/`: Python / FastAPI orchestration engine.
- `frontend/`: Next.js 14 premium investigation workspace with React Three Fiber (R3F) 3D telemetry visualization.
- `presentation/`: Standalone Next.js marketing and storytelling website.
- `docs/`: In-depth architectural & API documentation.

---

## 🛠 Local Setup & Running Tests

### 1. Environment Configuration
Copy `.env.example` to `.env`:
```bash
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
FIRESTORE_DATABASE_ID=(default)
CORS_ORIGINS=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 2. Backend Setup & Tests
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python3 -m pytest tests -v
```

### 3. Start Servers
```bash
# Start FastAPI backend
cd backend
uvicorn main:app --reload --port 8000

# Start Next.js frontend (in another terminal)
cd frontend
npm install
npm run dev

# Start Presentation Website (in another terminal)
cd presentation
npm install
npm run dev
```

---

## ☁️ Deployment & Demo Status

VERDICT is fully containerized and Cloud Run deployment-ready. 
**Live Demo:** Cloud Run deployment pending external Google Cloud billing/account verification.

---

## 📄 License

Distributed under the [MIT License](LICENSE).
