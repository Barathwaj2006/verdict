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
        self._local_docs: Dict[str, Any] = {}
        self._local_rounds: Dict[str, Dict[str, Any]] = {}
        self._local_state: Dict[str, Dict[str, Any]] = {}
        
        # In a real environment with auth, initializing the client may require correct auth.
        # If emulator is set, it bypasses auth.
        self.db = None
        try:
            if self.project_id:
                self.db = firestore.Client(project=self.project_id)
            else:
                self.db = firestore.Client()
        except Exception as e:
            print(f"Firestore client initialization warning: {e}")
            self.db = None
            
    def _handle_firestore_error(self, operation: str, error: Exception):
        err_msg = str(error)
        if "403" in err_msg or "PERMISSION_DENIED" in err_msg or "SERVICE_DISABLED" in err_msg:
            if self.db is not None:
                print(f"Firestore API is disabled/permission denied in project {self.project_id}. Falling back to in-memory persistence.")
                self.db = None
        else:
            print(f"Firestore {operation} warning (using local fallback): {error}")

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
        data = {
            "investigation_id": investigation_id,
            "original_objective": original_objective,
            "constraints": constraints,
            "status": "IN_PROGRESS",
            "current_round": 1,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._local_docs[investigation_id] = data.copy()
        if self.db:
            try:
                doc_ref = self.db.collection("investigations").document(investigation_id)
                doc_ref.set({
                    **data,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "updated_at": firestore.SERVER_TIMESTAMP,
                })
            except Exception as e:
                self._handle_firestore_error("write", e)
        
    def get_investigation_metadata(self, investigation_id: str) -> Optional[Dict[str, Any]]:
        if self.db:
            try:
                doc_ref = self.db.collection("investigations").document(investigation_id)
                doc = doc_ref.get()
                if doc.exists:
                    return doc.to_dict()
            except Exception as e:
                self._handle_firestore_error("read", e)
        return self._local_docs.get(investigation_id)
        
    def update_investigation_status(self, investigation_id: str, status: str, current_round: int = None, termination_reason: str = None):
        if investigation_id in self._local_docs:
            self._local_docs[investigation_id]["status"] = status
            self._local_docs[investigation_id]["updated_at"] = datetime.utcnow().isoformat()
            if current_round is not None:
                self._local_docs[investigation_id]["current_round"] = current_round
            if termination_reason is not None:
                self._local_docs[investigation_id]["termination_reason"] = termination_reason
        if self.db:
            try:
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
            except Exception as e:
                self._handle_firestore_error("update", e)

    def save_round_start(self, investigation_id: str, round_number: int, plan: LeadPlan):
        round_key = f"{investigation_id}_{round_number}"
        if investigation_id not in self._local_rounds:
            self._local_rounds[investigation_id] = {}
        round_data = {
            "round_number": round_number,
            "status": "STARTED",
            "started_at": datetime.utcnow().isoformat(),
            "lead_plan": self._clean_dict(plan.model_dump(mode="json"))
        }
        self._local_rounds[investigation_id][round_key] = round_data
        if self.db:
            try:
                round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
                round_ref.set({
                    **round_data,
                    "started_at": firestore.SERVER_TIMESTAMP,
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("round start", e)
        
    def save_research_batch(self, investigation_id: str, round_number: int, batch: ResearchBatch):
        round_key = f"{investigation_id}_{round_number}"
        if investigation_id not in self._local_rounds:
            self._local_rounds[investigation_id] = {}
        if round_key not in self._local_rounds[investigation_id]:
            self._local_rounds[investigation_id][round_key] = {}
        self._local_rounds[investigation_id][round_key].update({
            "research_batch": self._clean_dict(batch.model_dump(mode="json")),
            "status": "RESEARCH_COMPLETED",
            "updated_at": datetime.utcnow().isoformat()
        })
        if self.db:
            try:
                round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
                round_ref.set({
                    "research_batch": self._clean_dict(batch.model_dump(mode="json")),
                    "status": "RESEARCH_COMPLETED",
                    "updated_at": firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("research batch", e)
        
    def save_skeptic_report(self, investigation_id: str, round_number: int, report: SkepticReport):
        round_key = f"{investigation_id}_{round_number}"
        if investigation_id not in self._local_rounds:
            self._local_rounds[investigation_id] = {}
        if round_key not in self._local_rounds[investigation_id]:
            self._local_rounds[investigation_id][round_key] = {}
        self._local_rounds[investigation_id][round_key].update({
            "skeptic_report": self._clean_dict(report.model_dump(mode="json")),
            "status": "SKEPTIC_COMPLETED",
            "updated_at": datetime.utcnow().isoformat()
        })
        if self.db:
            try:
                round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
                round_ref.set({
                    "skeptic_report": self._clean_dict(report.model_dump(mode="json")),
                    "status": "SKEPTIC_COMPLETED",
                    "updated_at": firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("skeptic report", e)
        
    def save_verification_result(self, investigation_id: str, round_number: int, verifications: List[VerificationResult]):
        round_key = f"{investigation_id}_{round_number}"
        serialized = [self._clean_dict(v.model_dump(mode="json")) for v in verifications]
        if investigation_id not in self._local_rounds:
            self._local_rounds[investigation_id] = {}
        if round_key not in self._local_rounds[investigation_id]:
            self._local_rounds[investigation_id][round_key] = {}
        self._local_rounds[investigation_id][round_key].update({
            "verification_results": serialized,
            "status": "VERIFICATION_COMPLETED",
            "updated_at": datetime.utcnow().isoformat()
        })
        if self.db:
            try:
                round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
                round_ref.set({
                    "verification_results": serialized,
                    "status": "VERIFICATION_COMPLETED",
                    "updated_at": firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("verification result", e)
        
    def save_round_decision(self, investigation_id: str, round_number: int, decision: str, knowledge_gaps: List[Any]):
        round_key = f"{investigation_id}_{round_number}"
        serialized_gaps = [self._clean_dict(gap.model_dump(mode="json")) for gap in knowledge_gaps]
        if investigation_id not in self._local_rounds:
            self._local_rounds[investigation_id] = {}
        if round_key not in self._local_rounds[investigation_id]:
            self._local_rounds[investigation_id][round_key] = {}
        self._local_rounds[investigation_id][round_key].update({
            "decision": decision,
            "knowledge_gaps": serialized_gaps,
            "status": "EVALUATED",
            "completed_at": datetime.utcnow().isoformat()
        })
        if self.db:
            try:
                round_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").document(f"round_{round_number}")
                round_ref.set({
                    "decision": decision,
                    "knowledge_gaps": serialized_gaps,
                    "status": "EVALUATED",
                    "completed_at": firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("round decision", e)
        
    def save_executed_queries(self, investigation_id: str, queries: List[str]):
        if investigation_id not in self._local_state:
            self._local_state[investigation_id] = {}
        self._local_state[investigation_id]["executed_queries"] = queries
        if self.db:
            try:
                state_ref = self.db.collection("investigations").document(investigation_id).collection("state").document("global_state")
                state_ref.set({
                    "executed_queries": queries,
                    "updated_at": firestore.SERVER_TIMESTAMP
                }, merge=True)
            except Exception as e:
                self._handle_firestore_error("executed queries", e)
        
    def get_executed_queries(self, investigation_id: str) -> List[str]:
        if self.db:
            try:
                state_ref = self.db.collection("investigations").document(investigation_id).collection("state").document("global_state")
                doc = state_ref.get()
                if doc.exists:
                    return doc.to_dict().get("executed_queries", [])
            except Exception as e:
                self._handle_firestore_error("get queries", e)
        return self._local_state.get(investigation_id, {}).get("executed_queries", [])

    def save_final_verdict(self, investigation_id: str, verdict: FinalVerdict):
        if investigation_id in self._local_docs:
            self._local_docs[investigation_id]["final_verdict"] = self._clean_dict(verdict.model_dump(mode="json"))
            self._local_docs[investigation_id]["status"] = "COMPLETED"
            self._local_docs[investigation_id]["updated_at"] = datetime.utcnow().isoformat()
        if self.db:
            try:
                doc_ref = self.db.collection("investigations").document(investigation_id)
                doc_ref.update({
                    "final_verdict": self._clean_dict(verdict.model_dump(mode="json")),
                    "status": "COMPLETED",
                    "updated_at": firestore.SERVER_TIMESTAMP
                })
            except Exception as e:
                self._handle_firestore_error("save final verdict", e)
        
    def load_investigation_state(self, investigation_id: str) -> InvestigationState:
        data = None
        if self.db:
            try:
                doc_ref = self.db.collection("investigations").document(investigation_id)
                doc = doc_ref.get()
                if doc.exists:
                    data = doc.to_dict()
            except Exception as e:
                print(f"Firestore load investigation state error: {e}")
        
        if not data:
            data = self._local_docs.get(investigation_id)
            
        if not data:
            raise ValueError(f"Investigation {investigation_id} does not exist.")
            
        state = InvestigationState(
            investigation_id=data.get("investigation_id"),
            original_objective=data.get("original_objective"),
            current_round=data.get("current_round", 1),
            status=data.get("status", "IN_PROGRESS"),
            termination_reason=data.get("termination_reason")
        )
        
        state.all_queries = self.get_executed_queries(investigation_id)
        
        if self.db:
            try:
                rounds_ref = self.db.collection("investigations").document(investigation_id).collection("rounds").order_by("round_number").stream()
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
                        state.knowledge_gaps = gaps
                return state
            except Exception as e:
                print(f"Firestore stream rounds error: {e}")
                
        # Local rounds fallback
        local_rounds = self._local_rounds.get(investigation_id, {})
        for r_key, r_data in sorted(local_rounds.items()):
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
                state.knowledge_gaps = gaps
                
        return state
