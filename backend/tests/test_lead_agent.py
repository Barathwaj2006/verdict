import pytest
from unittest.mock import patch, MagicMock
from app.agents.lead.agent import LeadAgent
from app.models.lead_plan import LeadPlan

@pytest.fixture
def agent():
    return LeadAgent(api_key="dummy_key_for_tests")

@pytest.mark.skipif(not pytest.importorskip("google.genai").Client, reason="Skipping actual API calls if real key isn't provided, wait we'll just run them if key exists")
def test_lead_agent_clear_request():
    # Only run this if we have a real API key in the environment
    import os
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("No API key available")
        
    agent = LeadAgent()
    plan = agent.create_plan(
        objective="Find a good SaaS idea for a B2B AI tool. I have a background in enterprise sales.",
        constraints=["Max 1 month to build MVP", "Must be a subscription model"]
    )
    
    assert plan.plan_status == "READY_FOR_RESEARCH"
    assert len(plan.clarification_questions) == 0
    assert len(plan.research_missions) > 0

def test_lead_agent_ambiguous_request():
    import os
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("No API key available")
        
    agent = LeadAgent()
    plan = agent.create_plan(
        objective="Help me buy a car.",
        constraints=[]
    )
    
    # It should ask a clarification question
    assert plan.plan_status == "NEEDS_CLARIFICATION" or len(plan.clarification_questions) > 0

def test_lead_agent_hackathon_context():
    import os
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("No API key available")
        
    agent = LeadAgent()
    plan = agent.create_plan(
        objective="Find a winning project idea for this hackathon: https://devpost.com/software. I'm a solo developer.",
        constraints=["3 days to build"]
    )
    
    assert plan.plan_status == "READY_FOR_RESEARCH"
    roles = [mission.specialist_role.lower() for mission in plan.research_missions]
    assert any("feasibility" in role or "opportunity" in role or "landscape" in role or "hackathon" in role for role in roles)

def test_lead_agent_different_objective():
    import os
    if not os.environ.get("GEMINI_API_KEY"):
        pytest.skip("No API key available")
        
    agent = LeadAgent()
    plan = agent.create_plan(
        objective="Investigate whether our company should migrate from AWS to GCP.",
        constraints=["Budget is $50k", "Must not have downtime"]
    )
    
    roles = [mission.specialist_role.lower() for mission in plan.research_missions]
    assert plan.plan_status == "READY_FOR_RESEARCH"
    # Should dynamically generate missions, not just hackathon ones
    assert len(plan.research_missions) > 0

@patch('app.agents.lead.agent.genai.Client')
def test_lead_agent_malformed_output(mock_client):
    agent = LeadAgent(api_key="fake")
    mock_instance = mock_client.return_value
    
    # Create a mock response that raises an exception when parsed
    mock_response = MagicMock()
    mock_response.text = '{"malformed": "json"'
    mock_response.parsed = None
    
    mock_instance.models.generate_content.return_value = mock_response
    
    with pytest.raises(RuntimeError) as exc_info:
        agent.create_plan(objective="Do something")
    
    assert "LeadAgent generated malformed plan that failed validation" in str(exc_info.value)
