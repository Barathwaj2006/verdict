# API Reference & SSE Event Schema

VERDICT exposes REST endpoints and a Server-Sent Events (SSE) stream via FastAPI (`backend/main.py` and `backend/app/api/routes.py`).

---

## REST Endpoints

### 1. Health Check
`GET /health`
- **Response**: `{"status": "ok", "service": "verdict-backend"}`

---

### 2. Start Investigation
`POST /api/investigations`
- **Request Body**:
  ```json
  {
    "objective": "Should we migrate our backend to FastAPI?",
    "constraints": ["3-person team", "High performance needed"]
  }
  ```
- **Response**: `200 OK`
  ```json
  {
    "investigation_id": "inv_12345678",
    "status": "RUNNING",
    "current_round": 1
  }
  ```

---

### 3. Get Investigation Status
`GET /api/investigations/{investigation_id}`
- **Response**: Returns the complete `InvestigationState` object including rounds, claims, skeptic challenges, verifications, and final verdict (if completed).

---

### 4. Resume Investigation
`POST /api/investigations/{investigation_id}/resume`
- **Response**: Resumes an interrupted or multi-round investigation loop.

---

### 5. Get Final Verdict
`GET /api/investigations/{investigation_id}/verdict`
- **Response**: Returns the structured `FinalVerdict` object once completed.

---

## Server-Sent Events (SSE) Stream

`GET /api/investigations/{investigation_id}/events`

Broadcasts execution events in real time to frontend consumers.

### Event Format
```
data: {"event_type": "ROUND_START", "investigation_id": "inv_12345678", "data": {"round_number": 1}}

data: {"event_type": "LEAD_PLAN_CREATED", "investigation_id": "inv_12345678", "data": {...}}

data: {"event_type": "RESEARCH_COMPLETED", "investigation_id": "inv_12345678", "data": {...}}

data: {"event_type": "SKEPTIC_ATTACK_COMPLETED", "investigation_id": "inv_12345678", "data": {...}}

data: {"event_type": "VERIFICATION_COMPLETED", "investigation_id": "inv_12345678", "data": {...}}

data: {"event_type": "INVESTIGATION_COMPLETED", "investigation_id": "inv_12345678", "data": {...}}
```
