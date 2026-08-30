import os
import uuid
from typing import List, Optional

from app.models.investigation_state import InvestigationState, FinalVerdict
from app.models.lead_plan import LeadPlan
from app.agents.lead.agent import LeadAgent
from app.orchestration.research_orchestrator import ResearchOrchestrator
from app.agents.skeptic.agent import SkepticAgent
from app.agents.verifier.agent import VerifierAgent

from app.models.events import StreamingEvent, EventType
from app.services.event_bus import event_bus
from app.services.context_compressor import ContextCompressor
from app.services.firestore_repository import FirestoreRepository

class InvestigationController:
    def __init__(self, api_key: str = None, max_rounds: int = 3, repository: Optional[FirestoreRepository] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.max_rounds = max_rounds
        self.repository = repository
        
        # Sub-agents
        self.lead_agent = LeadAgent(api_key=self.api_key)
        self.research_orchestrator = ResearchOrchestrator(api_key=self.api_key)
        self.skeptic_agent = SkepticAgent(api_key=self.api_key)
        self.verifier_agent = VerifierAgent(api_key=self.api_key)

    async def resume_investigation(self, investigation_id: str) -> FinalVerdict:
        """Resumes an investigation from the repository."""
        if not self.repository:
            raise RuntimeError("Repository not provided. Cannot resume.")
            
        event_bus.publish(StreamingEvent(
            event_type=EventType.INVESTIGATION_STARTED,
            investigation_id=investigation_id,
            round_number=0,
            payload={"action": "resume"}
        ))
        
        state = self.repository.load_investigation_state(investigation_id)
        
        if state.status in ["COMPLETED", "FAILED"]:
            event_bus.publish(StreamingEvent(
                event_type=EventType.INVESTIGATION_COMPLETED,
                investigation_id=investigation_id,
                round_number=state.current_round,
                payload={"status": state.status}
            ))
            metadata = self.repository.get_investigation_metadata(investigation_id)
            if metadata and "final_verdict" in metadata:
                return FinalVerdict.model_validate(metadata["final_verdict"])
            return None # Should not happen if COMPLETED
            
        return await self._run_loop(state)

    async def run_investigation(self, objective: str, constraints: List[str] = None) -> FinalVerdict:
        investigation_id = f"inv_{uuid.uuid4().hex[:8]}"
        constraints = constraints or []
        
        event_bus.publish(StreamingEvent(
            event_type=EventType.INVESTIGATION_STARTED,
            investigation_id=investigation_id,
            round_number=1,
            payload={"objective": objective}
        ))
        
        if self.repository:
            self.repository.create_investigation(investigation_id, objective, constraints)
            
        state = InvestigationState(
            investigation_id=investigation_id,
            original_objective=objective,
            max_rounds=self.max_rounds
        )
        
        return await self._run_loop(state)

    async def _run_loop(self, state: InvestigationState) -> FinalVerdict:
        # Check if we were interrupted mid-round. For simplicity, we just resume from the lead plan step of the current round.
        # A more robust system would resume exactly at the stage it crashed.
        # But this suffices for M6 baseline.
        
        while state.current_round <= state.max_rounds:
            event_bus.publish(StreamingEvent(
                event_type=EventType.ROUND_STARTED,
                investigation_id=state.investigation_id,
                round_number=state.current_round
            ))
            
            # STEP 1: LEAD AGENT PLANNING
            # If the current round already has a plan (from resumed state), we reuse it.
            # Otherwise we generate a new one.
            if len(state.lead_plans) >= state.current_round:
                plan = state.lead_plans[state.current_round - 1]
            else:
                if state.current_round == 1:
                    plan = self.lead_agent.create_initial_plan(state.original_objective, [])
                else:
                    compressed_context = ContextCompressor.compress_state(state, state.lead_plans[-1])
                    plan = self.lead_agent.create_followup_plan(compressed_context, state.knowledge_gaps)
                    
                state.lead_plans.append(plan)
                if self.repository:
                    self.repository.save_round_start(state.investigation_id, state.current_round, plan)

            # STEP 2: RESEARCH ORCHESTRATION
            if len(state.research_batches) >= state.current_round:
                research_batch = state.research_batches[state.current_round - 1]
            else:
                executed_queries = set(state.all_queries)
                research_batch = await self.research_orchestrator.execute_plan(
                    plan, 
                    state.investigation_id, 
                    state.current_round,
                    executed_queries=executed_queries
                )
                state.research_batches.append(research_batch)
                
                # Trust query protector and add new queries
                for finding in research_batch.findings:
                    pass # We do not add anything here because executed_queries is a set. But if we need it in state:
                if self.repository:
                    self.repository.save_research_batch(state.investigation_id, state.current_round, research_batch)
                    
            # STEP 3: SKEPTIC AGENT
            if len(state.skeptic_reports) >= state.current_round:
                skeptic_report = state.skeptic_reports[state.current_round - 1]
            else:
                executed_queries = set(state.all_queries)
                skeptic_report = await self.skeptic_agent.evaluate_batch(
                    research_batch, 
                    plan,
                    executed_queries=executed_queries
                )
                state.skeptic_reports.append(skeptic_report)
                if self.repository:
                    self.repository.save_skeptic_report(state.investigation_id, state.current_round, skeptic_report)

            # STEP 4: VERIFIER AGENT
            if len(state.verification_results) >= state.current_round:
                verifications = state.verification_results[state.current_round - 1]
            else:
                executed_queries = set(state.all_queries)
                verifications = await self.verifier_agent.verify_batch(
                    research_batch, 
                    skeptic_report, 
                    plan,
                    executed_queries=executed_queries
                )
                state.verification_results.append(verifications)
                if self.repository:
                    self.repository.save_verification_result(state.investigation_id, state.current_round, verifications)

            # STEP 5: LEAD AGENT EVALUATION
            compressed_context = ContextCompressor.compress_state(state, plan)
            decision = self.lead_agent.evaluate_evidence(compressed_context, research_batch, skeptic_report, verifications)
            
            if self.repository:
                self.repository.save_round_decision(state.investigation_id, state.current_round, decision.decision, decision.knowledge_gaps)
            
            event_bus.publish(StreamingEvent(
                event_type=EventType.ROUND_COMPLETED,
                investigation_id=state.investigation_id,
                round_number=state.current_round,
                payload={"decision": decision.decision}
            ))

            if decision.decision in ["FINALIZE", "STALLED"]:
                state.status = decision.decision
                break
                
            state.knowledge_gaps = decision.knowledge_gaps
            state.current_round += 1
            if self.repository:
                self.repository.update_investigation_status(state.investigation_id, "IN_PROGRESS", current_round=state.current_round)

        # FINAL VERDICT
        compressed_context = ContextCompressor.compress_state(state, state.lead_plans[-1])
        final_verdict = self.lead_agent.produce_final_verdict(state)
        
        if state.current_round > state.max_rounds:
            final_verdict.termination_reason = "MAX_ROUNDS_REACHED"
        else:
            final_verdict.termination_reason = state.status
            
        event_bus.publish(StreamingEvent(
            event_type=EventType.INVESTIGATION_COMPLETED,
            investigation_id=state.investigation_id,
            round_number=state.current_round,
            payload={"termination_reason": final_verdict.termination_reason}
        ))
        
        if self.repository:
            self.repository.save_final_verdict(state.investigation_id, final_verdict)
            
        return final_verdict
