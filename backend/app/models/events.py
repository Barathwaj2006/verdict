from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import uuid
from enum import Enum

class EventType(str, Enum):
    INVESTIGATION_STARTED = "INVESTIGATION_STARTED"
    ROUND_STARTED = "ROUND_STARTED"
    RESEARCH_PLAN_CREATED = "RESEARCH_PLAN_CREATED"
    RESEARCH_MISSION_CREATED = "RESEARCH_MISSION_CREATED"
    RESEARCHER_STARTED = "RESEARCHER_STARTED"
    SEARCH_STARTED = "SEARCH_STARTED"
    SEARCH_COMPLETED = "SEARCH_COMPLETED"
    QUERY_DEDUPLICATED = "QUERY_DEDUPLICATED"
    CLAIM_CREATED = "CLAIM_CREATED"
    EVIDENCE_VALIDATED = "EVIDENCE_VALIDATED"
    EVIDENCE_REJECTED = "EVIDENCE_REJECTED"
    SKEPTIC_STARTED = "SKEPTIC_STARTED"
    CHALLENGE_CREATED = "CHALLENGE_CREATED"
    VERIFIER_STARTED = "VERIFIER_STARTED"
    VERIFICATION_STARTED = "VERIFICATION_STARTED"
    VERIFICATION_COMPLETED = "VERIFICATION_COMPLETED"
    LEAD_EVALUATION_STARTED = "LEAD_EVALUATION_STARTED"
    LEAD_DECISION = "LEAD_DECISION"
    KNOWLEDGE_GAP_IDENTIFIED = "KNOWLEDGE_GAP_IDENTIFIED"
    FOLLOWUP_MISSION_CREATED = "FOLLOWUP_MISSION_CREATED"
    ROUND_COMPLETED = "ROUND_COMPLETED"
    INVESTIGATION_COMPLETED = "INVESTIGATION_COMPLETED"
    INVESTIGATION_FAILED = "INVESTIGATION_FAILED"
    INVESTIGATION_STALLED = "INVESTIGATION_STALLED"
    MAX_ROUNDS_REACHED = "MAX_ROUNDS_REACHED"

class StreamingEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: f"evt_{uuid.uuid4().hex[:8]}")
    investigation_id: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    event_type: EventType
    round_number: Optional[int] = None
    agent: Optional[str] = None
    mission_id: Optional[str] = None
    claim_id: Optional[str] = None
    payload: Dict[str, Any] = Field(default_factory=dict)
