from app.orchestration.investigation_controller import InvestigationController
from app.services.firestore_repository import FirestoreRepository

_repo: FirestoreRepository = None
_controller: InvestigationController = None

def get_firestore_repository() -> FirestoreRepository:
    global _repo
    if _repo is None:
        _repo = FirestoreRepository()
    return _repo

def get_investigation_controller() -> InvestigationController:
    global _controller
    if _controller is None:
        _controller = InvestigationController(repository=get_firestore_repository())
    return _controller
