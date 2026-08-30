import pytest
import asyncio
from unittest.mock import patch, MagicMock
from app.agents.skeptic.agent import SkepticAgent, ClaimPrioritization
from app.agents.researchers.specialist import SearchQueryPlan
from app.models.research_finding import ResearchFinding, ResearchBatch, Claim
from app.models.lead_plan import LeadPlan
from app.models.skeptic_report import SkepticChallenge
from app.services.research_tool import ResearchTool, SearchResult

class MockSkepticSearchProvider(ResearchTool):
    def search(self, query: str, max_results: int = 3):
        if "fail" in query:
            raise RuntimeError("Search completely failed")
        if "contradict" in query:
            return [SearchResult(title="Truth", url="http://truth.com", snippet="Actually, it is false.", source_domain="truth.com")]
        return []

@pytest.fixture
def mock_lead_plan():
    return LeadPlan(
        investigation_objective="Test", user_requirements="Test", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=["Accuracy"], research_objectives=[],
        research_missions=[], required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY_FOR_RESEARCH"
    )

def create_claim(id, statement, source="http://source.com"):
    return Claim(
        claim_id=id, statement=statement, evidence="Some evidence", 
        source="EXTERNAL_SOURCE", source_urls=[source], confidence=0.9, status="UNVERIFIED"
    )

@pytest.mark.asyncio
@patch('app.agents.skeptic.agent.genai.Client')
async def test_skeptic_prioritization(mock_client, mock_lead_plan):
    mock_instance = mock_client.return_value
    
    # Mock prioritize
    mock_prio = MagicMock()
    mock_prio.parsed = ClaimPrioritization(selected_claim_ids=["c1", "c3"])
    
    # Mock challenge
    mock_chal = MagicMock()
    mock_chal.parsed = SkepticChallenge(
        claim_id="c1", original_claim="X", challenge_type="MISSING_CONTEXT",
        challenge_question="Y", counter_evidence="Z", counter_sources=[],
        reasoning_summary="R", severity="LOW", confidence=0.9, disposition="SUPPORTED"
    )
    
    def mock_generate_content(*args, **kwargs):
        schema = kwargs.get('config').response_schema
        if schema == ClaimPrioritization:
            return mock_prio
        elif schema == SearchQueryPlan:
            return MagicMock(parsed=MagicMock(queries=["q1"]))
        else:
            # We return a new MagicMock for SkepticChallenge so they don't overwrite
            m = MagicMock()
            m.parsed = SkepticChallenge(
                claim_id="c1", original_claim="X", challenge_type="MISSING_CONTEXT",
                challenge_question="Y", counter_evidence="Z", counter_sources=[],
                reasoning_summary="R", severity="LOW", confidence=0.9, disposition="SUPPORTED"
            )
            return m
            
    mock_instance.models.generate_content.side_effect = mock_generate_content
    
    agent = SkepticAgent(api_key="fake", search_provider=MockSkepticSearchProvider())
    batch = ResearchBatch(
        investigation_id="inv1", research_round=1,
        findings=[
            ResearchFinding(
                mission_id="m1", research_round=1, specialist_role="R",
                summary="S", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
                claims=[create_claim("c1", "C1"), create_claim("c2", "C2"), create_claim("c3", "C3")]
            )
        ]
    )
    
    report = await agent.evaluate_batch(batch, mock_lead_plan)
    
    # Should only have challenged c1 and c3
    assert len(report.challenges) == 2
    assert "c2" not in [c.claim_id for c in report.challenges]

@pytest.mark.asyncio
@patch('app.agents.skeptic.agent.genai.Client')
async def test_skeptic_never_verifies(mock_client, mock_lead_plan):
    mock_instance = mock_client.return_value
    
    mock_prio = MagicMock()
    mock_prio.parsed = ClaimPrioritization(selected_claim_ids=["c1"])
    
    mock_chal = MagicMock()
    # The model tries to VERIFY
    mock_chal.parsed = SkepticChallenge(
        claim_id="c1", original_claim="X", challenge_type="MISSING_CONTEXT",
        challenge_question="Y", counter_evidence="Z", counter_sources=[],
        reasoning_summary="R", severity="LOW", confidence=0.9, disposition="VERIFIED"
    )
    
    mock_instance.models.generate_content.side_effect = [
        mock_prio,
        MagicMock(parsed=MagicMock(queries=["q1"])), mock_chal
    ]
    
    agent = SkepticAgent(api_key="fake", search_provider=MockSkepticSearchProvider())
    batch = ResearchBatch(
        investigation_id="inv1", research_round=1,
        findings=[
            ResearchFinding(
                mission_id="m1", research_round=1, specialist_role="R",
                summary="S", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
                claims=[create_claim("c1", "C1")]
            )
        ]
    )
    
    report = await agent.evaluate_batch(batch, mock_lead_plan)
    # The agent code should forcefully override 'VERIFIED' to 'REQUIRES_VERIFICATION'
    assert report.challenges[0].disposition == "REQUIRES_VERIFICATION"

@pytest.mark.asyncio
@patch('app.agents.skeptic.agent.genai.Client')
async def test_skeptic_search_failure_graceful(mock_client, mock_lead_plan):
    mock_instance = mock_client.return_value
    
    mock_prio = MagicMock()
    mock_prio.parsed = ClaimPrioritization(selected_claim_ids=["c1"])
    
    mock_chal = MagicMock()
    mock_chal.parsed = SkepticChallenge(
        claim_id="c1", original_claim="X", challenge_type="INSUFFICIENT_EVIDENCE",
        challenge_question="Y", counter_evidence="None found due to search failure", counter_sources=[],
        reasoning_summary="R", severity="MEDIUM", confidence=0.5, disposition="WEAKENED"
    )
    
    # We inject 'fail' to trigger the exception in MockSkepticSearchProvider
    mock_instance.models.generate_content.side_effect = [
        mock_prio,
        MagicMock(parsed=MagicMock(queries=["fail test"])), mock_chal
    ]
    
    agent = SkepticAgent(api_key="fake", search_provider=MockSkepticSearchProvider())
    batch = ResearchBatch(
        investigation_id="inv1", research_round=1,
        findings=[
            ResearchFinding(
                mission_id="m1", research_round=1, specialist_role="R",
                summary="S", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
                claims=[create_claim("c1", "C1")]
            )
        ]
    )
    
    # Should not throw exception, should complete challenge
    report = await agent.evaluate_batch(batch, mock_lead_plan)
    assert len(report.challenges) == 1
    assert report.challenges[0].disposition == "WEAKENED"
