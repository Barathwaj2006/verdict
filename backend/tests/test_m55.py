import pytest
from app.services.evidence_integrity import EvidenceIntegrityValidator
from app.services.event_bus import EventBus
from app.models.events import StreamingEvent, EventType
from app.services.context_compressor import ContextCompressor
from app.models.investigation_state import InvestigationState, KnowledgeGap
from app.models.lead_plan import LeadPlan
from app.services.query_protector import DuplicateQueryProtector

def test_integrity_valid_url_accepted():
    res = EvidenceIntegrityValidator.validate_urls(["http://example.com"], ["http://example.com/"])
    assert res.valid
    assert len(res.accepted_urls) == 1

def test_integrity_hallucinated_rejected():
    res = EvidenceIntegrityValidator.validate_urls(["http://hallucination.com"], ["http://example.com"])
    assert not res.valid
    assert len(res.rejected_urls) == 1

def test_integrity_mixed():
    res = EvidenceIntegrityValidator.validate_urls(["http://hallucination.com", "http://example.com"], ["http://example.com"])
    assert not res.valid
    assert "http://example.com" in res.accepted_urls
    assert "http://hallucination.com" in res.rejected_urls

def test_integrity_model_knowledge_passes():
    res = EvidenceIntegrityValidator.validate_urls(["MODEL_KNOWLEDGE"], ["http://example.com"])
    assert res.valid
    assert "MODEL_KNOWLEDGE" not in res.rejected_urls

def test_event_bus():
    bus = EventBus()
    received = []
    def callback(evt):
        received.append(evt)
    
    bus.subscribe(callback)
    bus.publish(StreamingEvent(event_type=EventType.INVESTIGATION_STARTED, investigation_id="inv1"))
    
    assert len(received) == 1
    assert received[0].investigation_id == "inv1"
    
    def failing_callback(evt):
        raise ValueError("I failed")
        
    bus.subscribe(failing_callback)
    bus.publish(StreamingEvent(event_type=EventType.INVESTIGATION_STARTED, investigation_id="inv2"))
    
    # Should not crash
    assert len(received) == 2
    
def test_duplicate_query_protector():
    executed = {"search term"}
    queries = ["search term", "Search   Term!", "new query"]
    unique, dups = DuplicateQueryProtector.filter_queries(queries, executed)
    
    assert len(unique) == 1
    assert unique[0] == "new query"
    assert len(dups) == 2

def test_context_compression():
    state = InvestigationState(investigation_id="1", original_objective="obj", current_round=2)
    state.knowledge_gaps.append(KnowledgeGap(description="gap", why_it_matters="m", evidence_needed="e", priority="HIGH", recommended_research_direction="r"))
    plan = LeadPlan(investigation_objective="obj", user_requirements="", explicit_constraints=[], inferred_constraints=[], decision_criteria=[], research_objectives=[], research_missions=[], required_specialist_roles=[], evidence_requirements=[], initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY")
    
    comp = ContextCompressor.compress_state(state, plan)
    assert comp.investigation_objective == "obj"
    assert len(comp.active_knowledge_gaps) == 1
    assert comp.active_knowledge_gaps[0] == "gap"
    assert len(comp.previous_lead_decisions) == 1
