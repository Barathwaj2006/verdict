import pytest
from unittest.mock import MagicMock, patch
from app.agents.researchers.specialist import SpecialistResearcher, SearchQueryPlan
from app.services.research_tool import ResearchTool, SearchResult, DuckDuckGoSearchProvider
from app.models.research_finding import ResearchFinding, Claim
from app.models.lead_plan import ResearchMissionPlan

class MockSearchProvider(ResearchTool):
    def search(self, query: str, max_results: int = 3):
        if "fail" in query:
            raise RuntimeError("Simulated failure")
        if "empty" in query:
            return []
        return [
            SearchResult(title="Docs", url="http://docs.com", snippet="Important text", source_domain="docs.com"),
            SearchResult(title="Blog", url="http://blog.com", snippet="Other text", source_domain="blog.com")
        ]

@pytest.fixture
def mission():
    return ResearchMissionPlan(
        mission_id="m1",
        specialist_role="Test Role",
        objective="Find implementations of autonomous research systems",
        specific_questions=["Is it common?"],
        required_evidence=["Examples"],
        expected_output="Summary",
        priority="High"
    )

def test_duckduckgo_search_provider_empty():
    provider = DuckDuckGoSearchProvider()
    with patch.object(provider.ddgs, 'text', return_value=[]):
        results = provider.search("empty")
        assert len(results) == 0

def test_duckduckgo_search_provider_success():
    provider = DuckDuckGoSearchProvider()
    mock_results = [{"title": "t1", "href": "http://example.com/1", "body": "b1"}]
    with patch.object(provider.ddgs, 'text', return_value=mock_results):
        results = provider.search("query")
        assert len(results) == 1
        assert results[0].url == "http://example.com/1"
        assert results[0].source_domain == "example.com"

@patch('app.agents.researchers.specialist.genai.Client')
def test_specialist_researcher_evidence_acquisition(mock_client, mission):
    mock_instance = mock_client.return_value
    
    # Mock Step 1: Query generation
    mock_query_response = MagicMock()
    mock_query_response.parsed = SearchQueryPlan(queries=["autonomous research systems multi agent"])
    
    # Mock Step 3: Finding synthesis
    mock_finding_response = MagicMock()
    mock_finding_response.parsed = ResearchFinding(
        mission_id="m1", research_round=1, specialist_role="Test",
        summary="Found stuff", evidence=[], sources=[], confidence=0.9, unresolved_questions=[], limitations=[],
        claims=[Claim(statement="Systems exist", evidence="Docs say so", source="EXTERNAL_SOURCE", source_urls=["http://docs.com"], confidence=0.9)]
    )
    
    mock_instance.models.generate_content.side_effect = [mock_query_response, mock_finding_response]
    
    researcher = SpecialistResearcher(api_key="fake", search_provider=MockSearchProvider())
    finding = researcher.execute_mission(mission, "inv_1", 1)
    
    # Verify parsing
    assert len(finding.claims) == 1
    assert finding.claims[0].source_urls == ["http://docs.com"]
    assert finding.claims[0].status == "UNVERIFIED"

@patch('app.agents.researchers.specialist.genai.Client')
def test_specialist_researcher_search_failure(mock_client, mission):
    mock_instance = mock_client.return_value
    
    # Generate a query that triggers failure in mock
    mock_query_response = MagicMock()
    mock_query_response.parsed = SearchQueryPlan(queries=["fail test"])
    
    mock_finding_response = MagicMock()
    mock_finding_response.parsed = ResearchFinding(
        mission_id="m1", research_round=1, specialist_role="Test",
        summary="No results found", evidence=[], sources=[], confidence=0.5, unresolved_questions=[], limitations=[],
        claims=[Claim(statement="I think it exists", evidence="Model knowledge", source="MODEL_KNOWLEDGE", confidence=0.5)]
    )
    
    mock_instance.models.generate_content.side_effect = [mock_query_response, mock_finding_response]
    
    researcher = SpecialistResearcher(api_key="fake", search_provider=MockSearchProvider())
    finding = researcher.execute_mission(mission, "inv_1", 1)
    
    assert len(finding.claims) == 1
    assert finding.claims[0].source == "MODEL_KNOWLEDGE"

