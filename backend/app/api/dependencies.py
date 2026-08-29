from app.orchestration.investigation_controller import InvestigationController
from app.services.firestore_repository import FirestoreRepository

def get_firestore_repository() -> FirestoreRepository:
    return FirestoreRepository()

def get_investigation_controller() -> InvestigationController:
    return InvestigationController(repository=get_firestore_repository())
