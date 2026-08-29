from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class SkepticChallenge(BaseModel):
    challenge_id: str = Field(default_factory=lambda: f"challenge_{uuid.uuid4().hex[:8]}")
    claim_id: str
    original_claim: str
    challenge_type: str = Field(
        description="Must be one of: CONTRADICTORY_EVIDENCE, INSUFFICIENT_EVIDENCE, OUTDATED_SOURCE, SOURCE_QUALITY, LOGICAL_LEAP, MISSING_CONTEXT, COUNTEREXAMPLE, ASSUMPTION"
    )
    challenge_question: str
    counter_evidence: str
    counter_sources: List[str] = Field(default_factory=list)
    counter_source_titles: List[str] = Field(default_factory=list)
    reasoning_summary: str
    severity: str = Field(description="Must be one of: LOW, MEDIUM, HIGH, CRITICAL")
    confidence: float = Field(ge=0.0, le=1.0)
    disposition: str = Field(
        description="Must be one of: SUPPORTED, WEAKENED, CONTESTED, REQUIRES_VERIFICATION"
    )

class SkepticReport(BaseModel):
    investigation_id: str
    research_round: int
    challenges: List[SkepticChallenge]
