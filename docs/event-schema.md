# Event Schema (Server-Sent Events)

Events emitted by the backend to the frontend to visualize the autonomous process.

```typescript
type EventType = 
  | 'LEAD_AGENT_STARTED'
  | 'RESEARCH_PLAN_CREATED'
  | 'RESEARCHER_STARTED'
  | 'RESEARCHER_COMPLETED'
  | 'CLAIM_CREATED'
  | 'SKEPTIC_STARTED'
  | 'CLAIM_CHALLENGED'
  | 'VERIFIER_STARTED'
  | 'CLAIM_VERIFIED'
  | 'EVIDENCE_INSUFFICIENT'
  | 'KNOWLEDGE_GAP_FOUND'
  | 'RESEARCH_ROUND_STARTED'
  | 'VERDICT_READY';

interface ExecutionEvent {
  id: string;
  investigation_id: string;
  timestamp: string; // ISO 8601
  type: EventType;
  agent?: string; // e.g., 'Lead', 'Feasibility Researcher'
  payload: any; // Context-specific payload (e.g., the claim object, the challenge text, the verdict summary)
  message: string; // Human-readable summary for the UI timeline
}
```
