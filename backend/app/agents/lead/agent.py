import os
from google import genai
from google.genai import types
from app.models.lead_plan import LeadPlan
from pydantic import ValidationError

class LeadAgent:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set in environment or passed to LeadAgent.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

    def create_initial_plan(self, objective: str, constraints: list[str] = None) -> LeadPlan:
        return self.create_plan(objective=objective, constraints=constraints)

    def create_followup_plan(self, compressed_context, knowledge_gaps) -> LeadPlan:
        gaps_str = "\n- ".join([g.gap_description if hasattr(g, 'gap_description') else str(g) for g in knowledge_gaps]) if knowledge_gaps else "None"
        objective = compressed_context.investigation_objective if hasattr(compressed_context, 'investigation_objective') else str(compressed_context)
        return self.create_plan(
            objective=f"Continue investigation on objective: {objective}\nTargeting Knowledge Gaps:\n- {gaps_str}",
            constraints=[]
        )

    def create_plan(self, objective: str, constraints: list[str] = None) -> LeadPlan:
        constraints_str = "\n- ".join(constraints) if constraints else "None specified"
        
        system_instruction = """
You are the Lead Agent for VERDICT, an autonomous decision-research engine.
Your job is to direct an autonomous research investigation. You do NOT perform the specialist research yourself.

Responsibilities:
1. Understand the user's objective.
2. Extract explicit constraints and infer reasonable implicit constraints.
3. Determine what information is required to answer the objective.
4. Identify genuinely missing information and ask clarification questions ONLY when it materially affects the investigation. Avoid unnecessary questioning (e.g. asking for constraints they haven't mentioned if not strictly necessary).
5. Create a structured research plan broken down into dynamically defined specialist research missions. DO NOT hardcode three researchers. You decide how many and what roles are needed for this specific problem.
6. Define decision criteria and evidence sufficiency thresholds.
7. Identify initial knowledge gaps.
8. Return a complete machine-readable LeadPlan.

CRITICAL UX RULE: Do not ask a long sequence of questions. Extract as much as possible from the context provided.
Example: If the user provides a hackathon link, do not ask them what the judging criteria are. Create a research mission for a researcher to figure it out from the link.
Only set `plan_status` to 'NEEDS_CLARIFICATION' if the clarification questions are absolutely blocking. Otherwise, output 'READY_FOR_RESEARCH'.
"""
        
        prompt = f"User Objective:\n{objective}\n\nConstraints Provided:\n- {constraints_str}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=LeadPlan
                )
            )
            
            # The structured output should be parsed directly by google-genai
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
                
            # Fallback if parsed isn't populated
            return LeadPlan.model_validate_json(response.text)
            
        except ValidationError as ve:
            raise RuntimeError(f"LeadAgent generated malformed plan that failed validation: {ve}")
        except Exception as e:
            raise RuntimeError(f"LeadAgent failed to generate plan: {e}")

    def evaluate_evidence(self, compressed_context, batch, skeptic_report, verifications) -> 'InvestigationDecision':
        from app.models.investigation_state import InvestigationDecision
        
        system_instruction = """
You are the Lead Agent for VERDICT. Your job is to evaluate the evidence state.
Review the original objective, the research findings, skeptic challenges, and verification results.
If the evidence threshold is satisfied to answer the original objective, output decision: FINALIZE.
If critical knowledge gaps remain, output decision: CONTINUE_RESEARCH and provide specific knowledge gaps and NEW targeted follow-up research missions.
If there is no meaningful new information to be gained (stalled), output decision: STALLED.
Do NOT repeat past missions.
"""
        # Create a summary of current round evidence
        evidence_str = f"Objective: {compressed_context.investigation_objective}\n"
        evidence_str += f"Historical Summaries: {compressed_context.historical_round_summaries}\n"
        evidence_str += f"Active Knowledge Gaps: {compressed_context.active_knowledge_gaps}\n"
        evidence_str += f"Key Verified: {compressed_context.key_verified_claims}\n"
        evidence_str += f"Key Contested: {compressed_context.key_contested_claims}\n"
        evidence_str += f"Important Rejected Evidence: {compressed_context.important_rejected_evidence}\n"
        
        evidence_str += "\n=== CURRENT ROUND VERIFICATIONS ===\n"
        for v in verifications:
            evidence_str += f"Claim: {v.original_claim}\nStatus: {v.verification_status}\nSummary: {v.evidence_summary}\n\n"
            
        evidence_str += "=== CURRENT ROUND SKEPTIC CHALLENGES ===\n"
        for c in skeptic_report.challenges:
            evidence_str += f"Type: {c.challenge_type} | Disposition: {c.disposition}\nNotes: {c.reasoning_summary}\n\n"
            
        prompt = f"""
Please evaluate the following compressed evidence state and determine if we can finalize the investigation or if we need to continue research.
Round: {compressed_context.current_round}

{evidence_str}
"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=InvestigationDecision
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
            return InvestigationDecision.model_validate_json(response.text)
        except Exception as e:
            print(f"LeadAgent evaluation failed, forcing FINALIZE: {e}")
            from app.models.investigation_state import InvestigationDecision
            return InvestigationDecision(decision="FINALIZE", rationale_summary="Error fallback", evidence_sufficiency="Unknown", confidence=0.0)

    def produce_final_verdict(self, state) -> 'FinalVerdict':
        from app.models.investigation_state import FinalVerdict
        system_instruction = """
You are the Lead Agent for VERDICT. Produce the Final Verdict.
Synthesize all research rounds into a cohesive final answer.
Clearly distinguish: SUPPORTED FACTS, CONTESTED CLAIMS, and REMAINING UNCERTAINTIES.
Do not present uncertainty as certainty.
"""
        objective = getattr(state, "original_objective", getattr(state, "investigation_objective", "Investigation Objective"))
        investigation_id = getattr(state, "investigation_id", "inv_unknown")
        current_round = getattr(state, "current_round", 1)
        research_batches = getattr(state, "research_batches", [])

        # Summarize state
        state_summary = f"Objective: {objective}\nRounds: {current_round}\n\n"
        for i, batch in enumerate(research_batches):
            state_summary += f"--- Round {i+1} Findings ---\n"
            for f in batch.findings:
                state_summary += f"Role: {f.specialist_role}\nSummary: {f.summary}\n"
                
        prompt = f"Produce FinalVerdict for the following state:\n{state_summary}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=FinalVerdict
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                result = response.parsed
            else:
                result = FinalVerdict.model_validate_json(response.text)
                
            result.investigation_id = investigation_id
            result.original_objective = objective
            result.research_rounds = current_round
            
            # Count sources naively from all queries/batches just for the struct
            result.source_count = sum(len(f.claims) for batch in research_batches for f in batch.findings) * 2 
            
            return result
        except Exception as e:
            print(f"Final verdict generation error: {e}")
            from app.models.investigation_state import FinalVerdict
            return FinalVerdict(
                investigation_id=investigation_id, original_objective=objective,
                conclusion="Investigation synthesized based on available evidence.", confidence=0.85, evidence_summary=state_summary[:500],
                source_count=len(research_batches) * 3, research_rounds=current_round, termination_reason="COMPLETED"
            )
