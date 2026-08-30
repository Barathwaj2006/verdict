from pydantic import BaseModel, Field
from typing import List
import uuid

class EvidenceMatrixEntry(BaseModel):
    source_url: str
    source_title: str
    relationship: str = Field(
        description="Must be one of: SUPPORTS, CONTRADICTS, QUALIFIES, IRRELEVANT"
    )
    relevance: str = Field(description="Must be one of: HIGH, MEDIUM, LOW")
    source_quality: str = Field(description="Must be one of: HIGH, MEDIUM, LOW")
    notes: str

class VerificationResult(BaseModel):
    verification_id: str = Field(default_factory=lambda: f"verification_{uuid.uuid4().hex[:8]}")
    investigation_id: str
    research_round: int
    claim_id: str
    original_claim: str
    normalized_claim: str
    verification_status: str = Field(
        description="Must be one of: VERIFIED, PARTIALLY_VERIFIED, CONTESTED, REFUTED, INSUFFICIENT_EVIDENCE"
    )
    confidence: float = Field(ge=0.0, le=1.0)
    evidence_summary: str
    supporting_sources: List[str]
    contradicting_sources: List[str]
    qualifying_sources: List[str]
    evidence_matrix: List[EvidenceMatrixEntry]
    unresolved_questions: List[str]
    verification_notes: str
