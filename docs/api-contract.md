# API Contract (FastAPI)

## REST Endpoints

### `POST /api/v1/investigations`
Start a new investigation.
**Request**:
```json
{
  "objective": "Find the strongest project opportunity for this hackathon...",
  "constraints": ["solo developer", "3 days to build"]
}
```
**Response**:
```json
{
  "investigation_id": "inv_12345",
  "status": "STARTED"
}
```

### `GET /api/v1/investigations/{investigation_id}`
Retrieve the full state of an investigation.
**Response**:
Returns the `Investigation` aggregate object including all rounds, claims, and final verdict (if any).

### `GET /api/v1/investigations/{investigation_id}/events`
SSE (Server-Sent Events) endpoint to stream execution events to the frontend in real-time.

### `POST /api/v1/investigations/{investigation_id}/clarify`
Provide answers to Lead Agent's clarification questions.
**Request**:
```json
{
  "answers": [
    {
      "question_id": "q_1",
      "answer": "I have experience with Python."
    }
  ]
}
```
