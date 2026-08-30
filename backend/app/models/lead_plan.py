from pydantic import BaseModel, Field
from typing import List, Optional

class ResearchMissionPlan(BaseModel):
    mission_id: str
    specialist_role: str = Field(description="Role of the specialist, e.g., 'Feasibility Researcher', 'Opportunity Researcher', etc.")
    objective: str
    specific_questions: List[str]
    required_evidence: List[str]
    expected_output: str
    priority: str = Field(description="'High', 'Medium', or 'Low'")

class LeadPlan(BaseModel):
    investigation_objective: str
    user_requirements: str
    explicit_constraints: List[str]
    inferred_constraints: List[str]
    decision_criteria: List[str]
    research_objectives: List[str]
    research_missions: List[ResearchMissionPlan]
    required_specialist_roles: List[str]
    evidence_requirements: List[str]
    initial_knowledge_gaps: List[str]
    clarification_questions: List[str] = Field(description="Questions to ask the user ONLY IF genuinely required. Empty list if none.")
    plan_status: str = Field(description="'READY_FOR_RESEARCH' or 'NEEDS_CLARIFICATION'")
