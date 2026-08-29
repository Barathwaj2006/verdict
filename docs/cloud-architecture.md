# Cloud Architecture & Persistence

VERDICT is built for Google Cloud serverless infrastructure and Cloud Run readiness.

---

## Firestore Persistence Schema

VERDICT uses Google Cloud Firestore as its state store, recording investigation progress round-by-round to ensure state durability, resumability, and auditability.

### Collection: `investigations`
Document ID: `{investigation_id}`

```json
{
  "investigation_id": "inv_87654321",
  "objective": "Determine whether to adopt Rust for our microservices",
  "constraints": ["Team size: 5", "Timeline: Q3"],
  "status": "COMPLETED",
  "current_round": 2,
  "rounds": [
    {
      "round_number": 1,
      "lead_plan": { ... },
      "research_missions": [ ... ],
      "claims": [ ... ],
      "skeptic_challenges": [ ... ],
      "verifications": [ ... ]
    }
  ],
  "final_verdict": {
    "recommendation": "PROCEED",
    "confidence_score": 0.88,
    "key_findings": [ ... ],
    "tradeoffs": [ ... ]
  },
  "created_at": "2025-01-01T00:00:00Z",
  "updated_at": "2025-01-01T00:05:00Z"
}
```

---

## Google Cloud Run Readiness

The backend application is fully containerized and production-ready for deployment to Google Cloud Run.

### Container Configuration (`backend/Dockerfile`)
- Base image: `python:3.12-slim`
- Server startup: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Port exposure: Port dynamically passed via `$PORT` environment variable (defaults to 8000).

### Environment Variables
- `GEMINI_API_KEY`: Required for Gemini model access.
- `GOOGLE_CLOUD_PROJECT`: Google Cloud project identifier.
- `FIRESTORE_DATABASE_ID`: `(default)` or specific Firestore database ID.
- `CORS_ORIGINS`: Allowed origins for API requests (e.g., `http://localhost:3000` or production frontend URL).
