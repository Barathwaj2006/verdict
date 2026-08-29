import pytest
import asyncio
from unittest.mock import patch, MagicMock
from app.agents.verifier.agent import VerifierAgent, NormalizedClaim
from app.agents.researchers.specialist import SearchQueryPlan
from app.models.research_finding import ResearchFinding, ResearchBatch, Claim
from app.models.lead_plan import LeadPlan
from app.models.skeptic_report import SkepticChallenge, SkepticReport
from app.models.verification_result import VerificationResult, EvidenceMatrixEntry
from app.services.research_tool import ResearchTool, SearchResult

class MockVerifierSearchProvider(ResearchTool):
    def search(self, query: str, max_results: int = 3):
        if "fail" in query:
            raise RuntimeError("Search completely failed")
        if "empty" in query:
            return []
        return [SearchResult(title="Docs", url="http://primary.com", snippet="Evidence", source_domain="primary.com")]

@pytest.fixture
def mock_lead_plan():
    return LeadPlan(
        investigation_objective="Test", user_requirements="Test", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=["Accuracy"], research_objectives=[],
        research_missions=[], required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY_FOR_RESEARCH"
    )

def create_claim(id, statement):
    return Claim(
        claim_id=id, statement=statement, evidence="Some evidence", 
        source="EXTERNAL_SOURCE", source_urls=["http://source.com"], confidence=0.9, status="UNVERIFIED"
    )

@pytest.mark.asyncio
@patch('app.agents.verifier.agent.genai.Client')
async def test_verifier_requires_external_sources_for_verified(mock_client, mock_lead_plan):
    mock_instance = mock_client.return_value
    
    mock_norm = MagicMock()
    mock_norm.parsed = NormalizedClaim(normalized_proposition="X")
    
    mock_result = MagicMock()
    # Attempting to VERIFY without external sources
    mock_result.parsed = VerificationResult(
        investigation_id="inv1", research_round=1, claim_id="c1", original_claim="X",
        normalized_claim="X", verification_status="VERIFIED", confidence=0.9, evidence_summary="Internal knowledge",
        supporting_sources=[], contradicting_sources=[], qualifying_sources=[], evidence_matrix=[],
        unresolved_questions=[], verification_notes=""
    )
    
    def mock_generate_content(*args, **kwargs):
        schema = kwargs.get('config').response_schema
        if schema == NormalizedClaim: return mock_norm
        if schema == SearchQueryPlan: return MagicMock(parsed=MagicMock(queries=["q1"]))
        return mock_result
        
    mock_instance.models.generate_content.side_effect = mock_generate_content
    
    agent = VerifierAgent(api_key="fake", search_provider=MockVerifierSearchProvider())
    batch = ResearchBatch(
        investigation_id="inv1", research_round=1,
        findings=[ResearchFinding(mission_id="m1", research_round=1, specialist_role="R", summary="S", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[], claims=[create_claim("c1", "C1")])]
    )
    report = SkepticReport(investigation_id="inv1", research_round=1, challenges=[
        SkepticChallenge(claim_id="c1", original_claim="X", challenge_type="MISSING_CONTEXT", challenge_question="Y", counter_evidence="Z", counter_sources=[], reasoning_summary="R", severity="LOW", confidence=0.9, disposition="CONTESTED")
    ])
    
    verifications = await agent.verify_batch(batch, report, mock_lead_plan)
    
    assert len(verifications) == 1
    # Should override to INSUFFICIENT_EVIDENCE
    assert verifications[0].verification_status == "INSUFFICIENT_EVIDENCE"
    assert "Overridden" in verifications[0].verification_notes

@pytest.mark.asyncio
@patch('app.agents.verifier.agent.genai.Client')
async def test_verifier_search_failure_graceful(mock_client, mock_lead_plan):
    mock_instance = mock_client.return_value
    
    mock_norm = MagicMock()
    mock_norm.parsed = NormalizedClaim(normalized_proposition="X")
    
    mock_result = MagicMock()
    mock_result.parsed = VerificationResult(
        investigation_id="inv1", research_round=1, claim_id="c1", original_claim="X",
        normalized_claim="X", verification_status="INSUFFICIENT_EVIDENCE", confidence=0.5, evidence_summary="Search failed",
        supporting_sources=[], contradicting_sources=[], qualifying_sources=[], evidence_matrix=[],
        unresolved_questions=[], verification_notes=""
    )
    
    def mock_generate_content(*args, **kwargs):
        schema = kwargs.get('config').response_schema
        if schema == NormalizedClaim: return mock_norm
        if schema == SearchQueryPlan: return MagicMock(parsed=MagicMock(queries=["fail test"]))
        return mock_result
        
    mock_instance.models.generate_content.side_effect = mock_generate_content
    
    agent = VerifierAgent(api_key="fake", search_provider=MockVerifierSearchProvider())
    batch = ResearchBatch(
        investigation_id="inv1", research_round=1,
        findings=[ResearchFinding(mission_id="m1", research_round=1, specialist_role="R", summary="S", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[], claims=[create_claim("c1", "C1")])]
    )
    report = SkepticReport(investigation_id="inv1", research_round=1, challenges=[
        SkepticChallenge(claim_id="c1", original_claim="X", challenge_type="MISSING_CONTEXT", challenge_question="Y", counter_evidence="Z", counter_sources=[], reasoning_summary="R", severity="LOW", confidence=0.9, disposition="CONTESTED")
    ])
    
    verifications = await agent.verify_batch(batch, report, mock_lead_plan)
    assert len(verifications) == 1
    assert verifications[0].verification_status == "INSUFFICIENT_EVIDENCE"
