from pydantic import BaseModel, Field
from typing import List, Optional, Any
import uuid
from datetime import datetime
from app.models.lead_plan import LeadPlan, ResearchMissionPlan
from app.models.research_finding import ResearchBatch
from app.models.skeptic_report import SkepticReport
from app.models.verification_result import VerificationResult

class KnowledgeGap(BaseModel):
    gap_id: str = Field(default_factory=lambda: f"gap_{uuid.uuid4().hex[:8]}")
    description: str
    affected_claim_ids: List[str] = Field(default_factory=list)
    why_it_matters: str
    evidence_needed: str
    priority: str = Field(description="Must be HIGH, MEDIUM, or LOW")
    recommended_research_direction: str

class InvestigationDecision(BaseModel):
    decision: str = Field(description="Must be CONTINUE_RESEARCH, FINALIZE, or STALLED")
    rationale_summary: str
    evidence_sufficiency: str
    knowledge_gaps: List[KnowledgeGap] = Field(default_factory=list)
    follow_up_missions: List[ResearchMissionPlan] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)

class FinalVerdict(BaseModel):
    investigation_id: str
    original_objective: str
    conclusion: str
    confidence: float
    key_findings: List[str] = Field(default_factory=list)
    verified_claims: List[str] = Field(default_factory=list)
    contested_claims: List[str] = Field(default_factory=list)
    unresolved_questions: List[str] = Field(default_factory=list)
    evidence_summary: str
    source_count: int
    research_rounds: int
    termination_reason: str

class InvestigationState(BaseModel):
    investigation_id: str
    original_objective: str
    current_round: int = 1
    max_rounds: int = 3
    lead_plans: List[LeadPlan] = Field(default_factory=list)
    research_batches: List[ResearchBatch] = Field(default_factory=list)
    skeptic_reports: List[SkepticReport] = Field(default_factory=list)
    verification_results: List[List[VerificationResult]] = Field(default_factory=list)
    knowledge_gaps: List[KnowledgeGap] = Field(default_factory=list)
    status: str = "PLANNING"
    termination_reason: Optional[str] = None
    all_queries: List[str] = Field(default_factory=list)
