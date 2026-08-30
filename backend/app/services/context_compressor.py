from pydantic import BaseModel, Field
from typing import List, Dict, Any
from app.models.investigation_state import InvestigationState
from app.models.lead_plan import LeadPlan

class CompressedInvestigationContext(BaseModel):
    investigation_objective: str
    user_constraints: List[str]
    current_round: int
    historical_round_summaries: List[str]
    active_knowledge_gaps: List[str]
    key_verified_claims: List[str]
    key_contested_claims: List[str]
    important_rejected_evidence: List[str]
    previous_lead_decisions: List[str]

class ContextCompressor:
    @staticmethod
    def compress_state(state: InvestigationState, latest_plan: LeadPlan) -> CompressedInvestigationContext:
        historical_summaries = []
        verified = []
        contested = []
        rejected = []
        
        # We summarize everything BEFORE the current round.
        for i in range(state.current_round - 1):
            batch = state.research_batches[i] if i < len(state.research_batches) else None
            summary = f"Round {i+1}: "
            if batch:
                summary += f"Found {sum(len(f.claims) for f in batch.findings)} claims."
            historical_summaries.append(summary)
            
        # Collect verified/contested from all verification results
        for round_verifications in state.verification_results:
            for v in round_verifications:
                if v.verification_status == "VERIFIED":
                    verified.append(v.normalized_claim)
                elif v.verification_status == "CONTESTED":
                    contested.append(v.normalized_claim)
                elif v.verification_status == "INSUFFICIENT_EVIDENCE" and "Overridden" in v.verification_notes:
                    rejected.append(f"Rejected hallucinated source for: {v.normalized_claim}")
                    
        gaps = [g.description for g in state.knowledge_gaps]
        
        decisions = []
        if state.current_round > 1:
            decisions.append("Previous round determined evidence was INSUFFICIENT.")
            
        return CompressedInvestigationContext(
            investigation_objective=state.original_objective,
            user_constraints=latest_plan.explicit_constraints,
            current_round=state.current_round,
            historical_round_summaries=historical_summaries,
            active_knowledge_gaps=gaps,
            key_verified_claims=verified,
            key_contested_claims=contested,
            important_rejected_evidence=rejected,
            previous_lead_decisions=decisions
        )
