import pytest
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock

from app.orchestration.investigation_controller import InvestigationController
from app.models.investigation_state import InvestigationDecision, KnowledgeGap, FinalVerdict
from app.models.lead_plan import LeadPlan, ResearchMissionPlan
from app.models.research_finding import ResearchBatch, ResearchFinding, Claim
from app.models.skeptic_report import SkepticReport
from app.models.verification_result import VerificationResult

@pytest.fixture
def mock_lead():
    with patch('app.orchestration.investigation_controller.LeadAgent') as mock:
        yield mock.return_value

@pytest.fixture
def mock_orchestrator():
    with patch('app.orchestration.investigation_controller.ResearchOrchestrator') as mock:
        instance = mock.return_value
        instance.execute_plan = AsyncMock()
        yield instance

@pytest.fixture
def mock_skeptic():
    with patch('app.orchestration.investigation_controller.SkepticAgent') as mock:
        instance = mock.return_value
        instance.evaluate_batch = AsyncMock()
        yield instance

@pytest.fixture
def mock_verifier():
    with patch('app.orchestration.investigation_controller.VerifierAgent') as mock:
        instance = mock.return_value
        instance.verify_batch = AsyncMock()
        yield instance

@pytest.mark.asyncio
async def test_controller_round1_sufficient(mock_lead, mock_orchestrator, mock_skeptic, mock_verifier):
    controller = InvestigationController()
    controller.lead_agent = mock_lead
    controller.research_orchestrator = mock_orchestrator
    controller.skeptic_agent = mock_skeptic
    controller.verifier_agent = mock_verifier
    
    mock_lead.create_initial_plan.return_value = LeadPlan(
        investigation_objective="Test", user_requirements="", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=[], research_objectives=[],
        research_missions=[], required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY"
    )
    
    mock_orchestrator.execute_plan.return_value = ResearchBatch(investigation_id="inv1", research_round=1, findings=[])
    mock_skeptic.evaluate_batch.return_value = SkepticReport(investigation_id="inv1", research_round=1, challenges=[])
    mock_verifier.verify_batch.return_value = []
    
    mock_lead.evaluate_evidence.return_value = InvestigationDecision(
        decision="FINALIZE", rationale_summary="All good", evidence_sufficiency="Yes", confidence=1.0
    )
    mock_lead.produce_final_verdict.return_value = FinalVerdict(
        investigation_id="inv1", original_objective="Test", conclusion="Done", confidence=1.0,
        key_findings=[], verified_claims=[], contested_claims=[], unresolved_questions=[], evidence_summary="",
        source_count=0, research_rounds=1, termination_reason="FINALIZE"
    )
    
    verdict = await controller.run_investigation("Test")
    assert verdict.research_rounds == 1
    assert verdict.termination_reason == "FINALIZE"

@pytest.mark.asyncio
async def test_controller_round2_continuation_then_finalize(mock_lead, mock_orchestrator, mock_skeptic, mock_verifier):
    controller = InvestigationController()
    controller.lead_agent = mock_lead
    controller.research_orchestrator = mock_orchestrator
    controller.skeptic_agent = mock_skeptic
    controller.verifier_agent = mock_verifier
    
    mock_lead.create_initial_plan.return_value = LeadPlan(
        investigation_objective="Test", user_requirements="", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=[], research_objectives=[],
        research_missions=[], required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY"
    )
    mock_lead.create_followup_plan.return_value = mock_lead.create_initial_plan.return_value
    
    # Round 1 decision: CONTINUE_RESEARCH
    # Round 2 decision: FINALIZE
    mock_lead.evaluate_evidence.side_effect = [
        InvestigationDecision(decision="CONTINUE_RESEARCH", rationale_summary="Need more", evidence_sufficiency="No", confidence=0.5, knowledge_gaps=[]),
        InvestigationDecision(decision="FINALIZE", rationale_summary="All good", evidence_sufficiency="Yes", confidence=1.0)
    ]
    
    mock_lead.produce_final_verdict.return_value = FinalVerdict(
        investigation_id="inv1", original_objective="Test", conclusion="Done", confidence=1.0,
        key_findings=[], verified_claims=[], contested_claims=[], unresolved_questions=[], evidence_summary="",
        source_count=0, research_rounds=2, termination_reason="FINALIZE"
    )
    
    verdict = await controller.run_investigation("Test")
    assert verdict.research_rounds == 2
    assert verdict.termination_reason == "FINALIZE"
    assert mock_lead.evaluate_evidence.call_count == 2

@pytest.mark.asyncio
async def test_controller_max_rounds(mock_lead, mock_orchestrator, mock_skeptic, mock_verifier):
    controller = InvestigationController(max_rounds=2)
    controller.lead_agent = mock_lead
    controller.research_orchestrator = mock_orchestrator
    controller.skeptic_agent = mock_skeptic
    controller.verifier_agent = mock_verifier
    
    mock_lead.create_initial_plan.return_value = LeadPlan(
        investigation_objective="Test", user_requirements="", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=[], research_objectives=[],
        research_missions=[], required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY"
    )
    mock_lead.create_followup_plan.return_value = mock_lead.create_initial_plan.return_value
    
    # Always return CONTINUE_RESEARCH
    mock_lead.evaluate_evidence.return_value = InvestigationDecision(
        decision="CONTINUE_RESEARCH", rationale_summary="Need more", evidence_sufficiency="No", confidence=0.5
    )
    
    mock_lead.produce_final_verdict.return_value = FinalVerdict(
        investigation_id="inv1", original_objective="Test", conclusion="Done", confidence=1.0,
        key_findings=[], verified_claims=[], contested_claims=[], unresolved_questions=[], evidence_summary="",
        source_count=0, research_rounds=2, termination_reason="MAX_ROUNDS_REACHED"
    )
    
    verdict = await controller.run_investigation("Test")
    assert verdict.research_rounds == 2
    assert verdict.termination_reason == "MAX_ROUNDS_REACHED"
    assert mock_orchestrator.execute_plan.call_count == 2
