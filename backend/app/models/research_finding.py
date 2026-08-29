from pydantic import BaseModel, Field
from typing import List, Optional
import uuid

class Claim(BaseModel):
    claim_id: str = Field(default_factory=lambda: f"claim_{uuid.uuid4().hex[:8]}")
    statement: str
    evidence: str
    source: str
    source_urls: List[str] = Field(default_factory=list)
    source_titles: List[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    status: str = Field(default="UNVERIFIED", description="Must start as UNVERIFIED")

class ResearchFinding(BaseModel):
    finding_id: str = Field(default_factory=lambda: f"finding_{uuid.uuid4().hex[:8]}")
    mission_id: str
    research_round: int
    specialist_role: str
    summary: str
    claims: List[Claim]
    evidence: List[str]
    sources: List[str]
    confidence: float = Field(ge=0.0, le=1.0)
    unresolved_questions: List[str]
    limitations: List[str]

class ResearchBatch(BaseModel):
    investigation_id: str
    research_round: int
    findings: List[ResearchFinding]
    errors: List[str] = Field(default_factory=list)
