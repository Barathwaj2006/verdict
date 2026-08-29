import os
from datetime import datetime
from typing import Optional, List, Dict, Any
from google.cloud import firestore

from app.models.investigation_state import InvestigationState, FinalVerdict
from app.models.lead_plan import LeadPlan
from app.models.research_finding import ResearchBatch
from app.models.skeptic_report import SkepticReport
from app.models.verification_result import VerificationResult

class FirestoreRepository:
    def __init__(self, project_id: Optional[str] = None):
        # Native google-cloud-firestore will automatically pick up:
        # FIRESTORE_EMULATOR_HOST, GOOGLE_APPLICATION_CREDENTIALS, GOOGLE_CLOUD_PROJECT
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        
        # In a real environment with auth, initializing the client may require correct auth.
        # If emulator is set, it bypasses auth.
        try:
            if self.project_id:
                self.db = firestore.Client(project=self.project_id)
            else:
                self.db = firestore.Client()
        except Exception as e:
            print(f"Failed to initialize Firestore client: {e}")
            raise RuntimeError(
                f"Firestore initialization failed: {e}\n\n"
                "To run this locally, you must authenticate with Google Cloud Application Default Credentials (ADC).\n"
                "Run the following commands:\n"
                "1. gcloud init (to select your project)\n"
                "2. gcloud auth application-default login\n"
            )
            
    def _clean_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively removes None values from a dict, as Firestore doesn't like some None fields or we just want to save space."""
        cleaned = {}
        for k, v in data.items():
            if v is None:
                continue
            if isinstance(v, dict):
                cleaned[k] = self._clean_dict(v)
            elif isinstance(v, list):
                cleaned_list = []
                for item in v:
                    if isinstance(item, dict):
                        cleaned_list.append(self._clean_dict(item))
                    else:
                        cleaned_list.append(item)
                cleaned[k] = cleaned_list
            else:
                cleaned[k] = v
        return cleaned

    def create_investigation(self, investigation_id: str, original_objective: str, constraints: List[str]):
        doc_ref = self.db.collection("investigations").document(investigation_id)
        doc_ref.set({
            "investigation_id": investigation_id,
            "original_objective": original_objective,
            "constraints": constraints,
            "status": "IN_PROGRESS",
            "current_round": 1,
            "created_at": firestore.SERVER_TIMESTAMP,
            "updated_at": firestore.SERVER_TIMESTAMP,
        })
        
    def get_investigation_metadata(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        doc_ref = self.db.collection("investigations").document(investigation_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        return None
        
    def update_investigation_status(self, investigation_id: str, status: str, current_round: int = None, termination_reason: str = None):
        doc_ref = self.db.collection("investigations").document(investigation_id)
        update_data = {
            "status": status,
            "updated_at": firestore.SERVER_TIMESTAMP
        }
        if current_round is not None:
            update_data["current_round"] = current_round
        if termination_reason is not None:
            update_data["termination_reason"] = termination_reason
            
        doc_ref.update(update_data)

    def save_round_start(self, investigation_id: str, round_number: int, plan: LeadPlan):
        round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
        round_ref.set({
            "round_number": round_number,
            "status": "STARTED",
            "started_at": firestore.SERVER_TIMESTAMP,
            "lead_plan": self._clean_dict(plan.model_dump(mode="json"))
        }, merge=True)
        
    def save_research_batch(self, investigation_id: str, round_number: int, batch: ResearchBatch):
        round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
        round_ref.set({
            "research_batch": self._clean_dict(batch.model_dump(mode="json")),
            "status": "RESEARCH_COMPLETED",
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    def save_skeptic_report(self, investigation_id: str, round_number: int, report: SkepticReport):
        round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
        round_ref.set({
            "skeptic_report": self._clean_dict(report.model_dump(mode="json")),
            "status": "SKEPTIC_COMPLETED",
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    def save_verification_result(self, investigation_id: str, round_number: int, verifications: List[VerificationResult]):
        round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
        serialized_verifications = [self._clean_dict(v.model_dump(mode="json")) for v in verifications]
        round_ref.set({
            "verification_results": serialized_verifications,
            "status": "VERIFICATION_COMPLETED",
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    def save_round_decision(self, investigation_id: str, round_number: int, decision: str, knowledge_gaps: List[Any]):
        round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
        serialized_gaps = [self._clean_dict(gap.model_dump(mode="json")) for gap in knowledge_gaps]
        round_ref.set({
            "decision": decision,
            "knowledge_gaps": serialized_gaps,
            "status": "EVALUATED",
            "completed_at": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    def save_executed_queries(self, investigation_id: str, queries: List[str]):
        state_ref = self.db.collection("investigations").document(investigation_id).collection("state").document("global_state")
        state_ref.set({
            "executed_queries": queries,
            "updated_at": firestore.SERVER_TIMESTAMP
        }, merge=True)
        
    def get_executed_queries(self, investigation_id: str) -> List[str]:
        state_ref = self.db.collection("investigations").document(investigation_id).collection("state").document("global_state")
        doc = state_ref.get()
        if doc.exists:
            return doc.to_dict().get("executed_queries", [])
        return []

    def save_final_verdict(self, investigation_id: str, verdict: FinalVerdict):
        doc_ref = self.db.collection("investigations").document(investigation_id)
        doc_ref.update({
            "final_verdict": self._clean_dict(verdict.model_dump(mode="json")),
            "status": "COMPLETED",
            "updated_at": firestore.SERVER_TIMESTAMP
        })
        
    def load_investigation_state(self, investigation_id: str) -> InvestigationState:
        doc_ref = self.db.collection("investigations").document(investigation_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise ValueError(f"Investigation {investigation_id} does not exist.")
            
        data = doc.to_dict()
        
        state = InvestigationState(
            investigation_id=data.get("investigation_id"),
            original_objective=data.get("original_objective"),
            current_round=data.get("current_round", 1),
            status=data.get("status", "IN_PROGRESS"),
            termination_reason=data.get("termination_reason")
        )
        
        state.all_queries = self.get_executed_queries(investigation_id)
        
        rounds_ref = doc_ref.collection("rounds").order_by("round_number").stream()
        for r_doc in rounds_ref:
            r_data = r_doc.to_dict()
            
            if "lead_plan" in r_data:
                state.lead_plans.append(LeadPlan.model_validate(r_data["lead_plan"]))
                
            if "research_batch" in r_data:
                state.research_batches.append(ResearchBatch.model_validate(r_data["research_batch"]))
                
            if "skeptic_report" in r_data:
                state.skeptic_reports.append(SkepticReport.model_validate(r_data["skeptic_report"]))
                
            if "verification_results" in r_data:
                verifications = [VerificationResult.model_validate(v) for v in r_data["verification_results"]]
                state.verification_results.append(verifications)
                
            if "knowledge_gaps" in r_data:
                from app.models.investigation_state import KnowledgeGap
                gaps = [KnowledgeGap.model_validate(g) for g in r_data["knowledge_gaps"]]
                state.knowledge_gaps = gaps # Replaces active knowledge gaps with the latest
                
        return state
