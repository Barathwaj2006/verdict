import pytest
from unittest.mock import MagicMock, patch
from app.services.firestore_repository import FirestoreRepository
from app.models.investigation_state import InvestigationState, FinalVerdict
from app.models.lead_plan import LeadPlan
from app.models.research_finding import ResearchBatch
from app.models.skeptic_report import SkepticReport
from app.models.verification_result import VerificationResult

@pytest.fixture
def repo():
    # Mock firestore client entirely so we don't need real DB
    with patch("app.services.firestore_repository.firestore.Client") as mock_client:
        r = FirestoreRepository(project_id="test")
        r.db = mock_client.return_value
        yield r

def test_create_investigation(repo):
    repo.create_investigation("inv_1", "objective", ["c1"])
    # Verify set was called
    repo.db.collection.assert_called_with("investigations")
    repo.db.collection().document.assert_called_with("inv_1")
    repo.db.collection().document().set.assert_called_once()
    
    args = repo.db.collection().document().set.call_args[0][0]
    assert args["investigation_id"] == "inv_1"
    assert args["original_objective"] == "objective"
    assert args["status"] == "IN_PROGRESS"

def test_save_round_start(repo):
    plan = LeadPlan(investigation_objective="obj", user_requirements="", explicit_constraints=[], inferred_constraints=[], decision_criteria=[], research_objectives=[], research_missions=[], required_specialist_roles=[], evidence_requirements=[], initial_knowledge_gaps=[], clarification_questions=[], plan_status="READY")
    repo.save_round_start("inv_1", 1, plan)
    repo.db.collection().document().collection().document.assert_called_with("round_1")
    repo.db.collection().document().collection().document().set.assert_called_once()

def test_load_investigation_state_missing(repo):
    mock_doc = MagicMock()
    mock_doc.exists = False
    repo.db.collection().document().get.return_value = mock_doc
    with pytest.raises(ValueError):
        repo.load_investigation_state("inv_1")

def test_load_investigation_state_success(repo):
    mock_doc = MagicMock()
    mock_doc.exists = True
    mock_doc.to_dict.return_value = {
        "investigation_id": "inv_1",
        "original_objective": "test",
        "current_round": 2,
        "status": "IN_PROGRESS"
    }
    repo.db.collection().document().get.return_value = mock_doc
    
    # Mock state query
    mock_state_doc = MagicMock()
    mock_state_doc.exists = True
    mock_state_doc.to_dict.return_value = {"executed_queries": ["Q1"]}
    repo.db.collection().document().collection().document().get.return_value = mock_state_doc
    
    # Mock rounds stream
    repo.db.collection().document().collection().order_by().stream.return_value = []
    
    state = repo.load_investigation_state("inv_1")
    assert state.investigation_id == "inv_1"
    assert state.current_round == 2
    assert state.original_objective == "test"
    assert "Q1" in state.all_queries
