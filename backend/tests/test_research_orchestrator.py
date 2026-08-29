import pytest
import asyncio
from unittest.mock import patch, MagicMock
from app.orchestration.research_orchestrator import ResearchOrchestrator
from app.agents.researchers.specialist import SpecialistResearcher, SearchQueryPlan
from app.models.lead_plan import LeadPlan, ResearchMissionPlan
from app.models.research_finding import ResearchFinding, Claim
from app.services.research_tool import ResearchTool

class MockSearchProvider(ResearchTool):
    def search(self, query: str, max_results: int = 3):
        return []

@pytest.fixture
def mock_lead_plan():
    return LeadPlan(
        investigation_objective="Test",
        user_requirements="Test",
        explicit_constraints=[],
        inferred_constraints=[],
        decision_criteria=[],
        research_objectives=[],
        research_missions=[],
        required_specialist_roles=[],
        evidence_requirements=[],
        initial_knowledge_gaps=[],
        clarification_questions=[],
        plan_status="READY_FOR_RESEARCH"
    )

def create_mission(id, role):
    return ResearchMissionPlan(
        mission_id=id,
        specialist_role=role,
        objective="Test objective",
        specific_questions=["Q1?"],
        required_evidence=["E1"],
        expected_output="Output",
        priority="High"
    )

@pytest.mark.asyncio
@patch.object(SpecialistResearcher, 'execute_mission')
async def test_concurrent_execution(mock_execute, mock_lead_plan):
    # Mocking successful researcher output
    def side_effect(mission, inv_id, round_num):
        return ResearchFinding(
            mission_id=mission.mission_id,
            research_round=round_num,
            specialist_role=mission.specialist_role,
            summary="Test summary",
            claims=[],
            evidence=[],
            sources=[],
            confidence=0.9,
            unresolved_questions=[],
            limitations=[]
        )
    mock_execute.side_effect = side_effect

    orchestrator = ResearchOrchestrator(api_key="fake")
    
    # Test 2 missions
    mock_lead_plan.research_missions = [create_mission("m1", "Role 1"), create_mission("m2", "Role 2")]
    batch = await orchestrator.execute_plan(mock_lead_plan, "inv_1", 1)
    assert len(batch.findings) == 2
    
    # Test 3 missions
    mock_lead_plan.research_missions = [create_mission("m1", "R1"), create_mission("m2", "R2"), create_mission("m3", "R3")]
    batch = await orchestrator.execute_plan(mock_lead_plan, "inv_1", 1)
    assert len(batch.findings) == 3

    # Test 5 missions
@pytest.mark.asyncio
async def test_concurrent_execution():
    orchestrator = ResearchOrchestrator(api_key="fake")
    orchestrator._researcher.search_provider = MockSearchProvider()
    
    plan = LeadPlan(
        investigation_objective="Test", user_requirements="", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=[], research_objectives=[],
        research_missions=[create_mission("m1", "Role1"), create_mission("m2", "Role2")],
        required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY"
    )
    
    with patch('app.agents.researchers.specialist.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        
        def mock_generate_content(*args, **kwargs):
            schema = kwargs.get('config').response_schema
            mock_res = MagicMock()
            if schema == SearchQueryPlan:
                mock_res.parsed = SearchQueryPlan(queries=["Q1"])
            else:
                mock_res.parsed = ResearchFinding(
                    mission_id="", research_round=1, specialist_role="",
                    summary="", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
                    claims=[]
                )
            return mock_res
            
        mock_instance.models.generate_content.side_effect = mock_generate_content
        orchestrator._researcher.client = mock_instance
        
        batch = await orchestrator.execute_plan(plan, "inv_1", 1)
        assert len(batch.findings) == 2

@pytest.mark.asyncio
async def test_researcher_failure_isolation():
    orchestrator = ResearchOrchestrator(api_key="fake")
    orchestrator._researcher.search_provider = MockSearchProvider()
    
    plan = LeadPlan(
        investigation_objective="Test", user_requirements="", explicit_constraints=[],
        inferred_constraints=[], decision_criteria=[], research_objectives=[],
        research_missions=[create_mission("m1", "Role1"), create_mission("m2", "Role2")],
        required_specialist_roles=[], evidence_requirements=[],
        initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY"
    )
    
    with patch('app.agents.researchers.specialist.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        call_count = 0
        def mock_generate_content(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count > 2: # Fail the second mission's synthesize call
                raise ValueError("Simulated API Error")
            schema = kwargs.get('config').response_schema
            mock_res = MagicMock()
            if schema == SearchQueryPlan:
                mock_res.parsed = SearchQueryPlan(queries=["Q"])
            else:
                mock_res.parsed = ResearchFinding(
                    mission_id="", research_round=1, specialist_role="",
                    summary="", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[], claims=[]
                )
            return mock_res
            
        mock_instance.models.generate_content.side_effect = mock_generate_content
        orchestrator._researcher.client = mock_instance
        
        batch = await orchestrator.execute_plan(plan, "inv_1", 1)
        assert len(batch.findings) == 1

@pytest.mark.asyncio
async def test_claims_default_unverified():
    researcher = SpecialistResearcher(api_key="fake")
    researcher.search_provider = MockSearchProvider()
    mission = create_mission("m1", "Test")
    
    with patch('app.agents.researchers.specialist.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        
        def mock_generate_content(*args, **kwargs):
            schema = kwargs.get('config').response_schema
            mock_res = MagicMock()
            if schema == SearchQueryPlan:
                mock_res.parsed = SearchQueryPlan(queries=["Q"])
            else:
                mock_res.parsed = ResearchFinding(
                    mission_id="m1", research_round=1, specialist_role="Test",
                    summary="", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
                    claims=[Claim(statement="X", evidence="Y", source="Z", confidence=0.9, status="VERIFIED")]
                )
            return mock_res
            
        mock_instance.models.generate_content.side_effect = mock_generate_content
        researcher.client = mock_instance

        finding = researcher.execute_mission(mission, "inv_1", 2)
        assert finding.claims[0].status == "UNVERIFIED"

@pytest.mark.asyncio
async def test_malformed_input():
    researcher = SpecialistResearcher(api_key="fake")
    researcher.search_provider = MockSearchProvider()
    with patch('app.agents.researchers.specialist.genai.Client') as MockClient:
        mock_instance = MockClient.return_value
        
        def mock_generate_content(*args, **kwargs):
            schema = kwargs.get('config').response_schema
            mock_res = MagicMock()
            if schema == SearchQueryPlan:
                mock_res.parsed = SearchQueryPlan(queries=["Q"])
            else:
                mock_res.parsed = None
                mock_res.text = "This is not JSON"
            return mock_res
            
        mock_instance.models.generate_content.side_effect = mock_generate_content
        researcher.client = mock_instance

        with pytest.raises(RuntimeError) as exc:
            researcher.execute_mission(create_mission("m1", "Test"), "inv_1", 1)

        assert "validate" in str(exc.value)
