# VERDICT API Contract

The API uses FastAPI and returns structured JSON.

## Endpoints

### 1. `GET /health`
Returns basic service health.
**Response**:
```json
{
  "status": "ok",
  "service": "verdict-api"
}
```

### 2. `POST /api/investigations`
Starts a new autonomous investigation in the background.
**Request**:
```json
{
  "objective": "Determine if fusion power is viable before 2040",
  "constraints": ["Must rely on peer-reviewed evidence"]
}
```
**Response**:
```json
{
  "investigation_id": "inv_123abc",
  "status": "STARTED"
}
```

### 3. `GET /api/investigations/{investigation_id}`
Returns metadata and status.
**Response**:
```json
{
  "investigation_id": "inv_123abc",
  "status": "IN_PROGRESS",
  "current_round": 1
}
```

### 4. `GET /api/investigations/{investigation_id}/stream`
Provides a Server-Sent Events (SSE) stream.
**Events**:
- `INVESTIGATION_STARTED`
- `ROUND_STARTED`
- `RESEARCH_COMPLETED`
- `SKEPTIC_COMPLETED`
- `ROUND_COMPLETED`
- `INVESTIGATION_COMPLETED`

### 5. `POST /api/investigations/{investigation_id}/resume`
Resumes an interrupted or stalled investigation.
**Response**:
```json
{
  "investigation_id": "inv_123abc",
  "status": "RESUMED"
}
```

### 6. `GET /api/investigations/{investigation_id}/verdict`
Returns the final generated verdict if the investigation has completed.
