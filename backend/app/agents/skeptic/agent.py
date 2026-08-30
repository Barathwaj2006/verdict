import os
import asyncio
from typing import List, Optional, Set
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from app.models.research_finding import ResearchBatch, Claim
from app.models.lead_plan import LeadPlan
from app.models.skeptic_report import SkepticChallenge, SkepticReport
from app.services.research_tool import ResearchTool, DuckDuckGoSearchProvider
from app.agents.researchers.specialist import SearchQueryPlan

from app.models.events import StreamingEvent, EventType
from app.services.event_bus import event_bus
from app.services.evidence_integrity import EvidenceIntegrityValidator
from app.services.query_protector import DuplicateQueryProtector

class ClaimPrioritization(BaseModel):
    selected_claim_ids: List[str]
    rationale: Optional[str] = None

class SkepticAgent:
    def __init__(self, api_key: str = None, model: str = None, search_provider: ResearchTool = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        self.search_provider = search_provider or DuckDuckGoSearchProvider()

    async def evaluate_batch(self, batch: ResearchBatch, plan: LeadPlan, executed_queries: Set[str] = None) -> SkepticReport:
        event_bus.publish(StreamingEvent(
            event_type=EventType.SKEPTIC_STARTED,
            investigation_id=batch.investigation_id,
            round_number=batch.research_round,
            agent="SkepticAgent"
        ))
        
        executed_queries = executed_queries if executed_queries is not None else set()
        
        # Step 1: Prioritize Claims
        prioritization = self._prioritize_claims(batch, plan)
        selected_claims = [c for f in batch.findings for c in f.claims if c.claim_id in prioritization.selected_claim_ids]
        
        loop = asyncio.get_running_loop()
        tasks = []
        for claim in selected_claims:
            tasks.append(loop.run_in_executor(None, self._evaluate_single_claim, claim, batch.investigation_id, batch.research_round, executed_queries))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        challenges = []
        for r in results:
            if isinstance(r, Exception):
                print(f"Warning: Skeptic failed on a claim: {r}")
            elif isinstance(r, SkepticChallenge):
                challenges.append(r)
                
        return SkepticReport(
            investigation_id=batch.investigation_id,
            research_round=batch.research_round,
            challenges=challenges
        )

    def _prioritize_claims(self, batch: ResearchBatch, plan: LeadPlan) -> ClaimPrioritization:
        system_instruction = """
You are the Skeptic Agent. Review the claims produced by the researchers.
Select the claims that are most critical to the Lead Agent's decision criteria.
Focus on claims that are highly consequential, surprising, or potential single points of failure.
"""
        claims_context = ""
        for f in batch.findings:
            for c in f.claims:
                claims_context += f"ID: {c.claim_id}\nClaim: {c.statement}\n\n"
                
        prompt = f"Decision Criteria: {plan.decision_criteria}\n\nClaims:\n{claims_context}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ClaimPrioritization
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
            return ClaimPrioritization.model_validate_json(response.text)
        except:
            # Fallback: challenge all claims
            return ClaimPrioritization(
                selected_claim_ids=[c.claim_id for f in batch.findings for c in f.claims],
                rationale="Fallback: evaluating all claims."
            )

    def _evaluate_single_claim(self, claim: Claim, inv_id: str, round_num: int, executed_queries: Set[str]) -> SkepticChallenge:
        # Step 2: Generate Adversarial Queries
        queries = self._generate_adversarial_queries(claim)
        
        unique_queries, duplicate_queries = DuplicateQueryProtector.filter_queries(queries.queries, executed_queries)
        for dq in duplicate_queries:
            event_bus.publish(StreamingEvent(
                event_type=EventType.QUERY_DEDUPLICATED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="SkepticAgent",
                payload={"query": dq}
            ))
            
        search_results = []
        for query in unique_queries:
            try:
                search_results.extend(self.search_provider.search(query, max_results=3))
            except Exception as e:
                print(f"Skeptic search failed for '{query}': {e}")
                
        retrieved_urls = [r.url for r in search_results]

        formatted_results = []
        for r in search_results:
            formatted_results.append(f"Title: {r.title}\nURL: {r.url}\nSnippet: {r.snippet}")
            
        results_context = "\n\n".join(formatted_results) if formatted_results else "No counter-evidence found via external search."

        # Step 4: Generate Challenge
        system_instruction = """
You are the Skeptic Agent. Your goal is to disprove or weaken the original claim using the Counter-Evidence provided.
If the counter-evidence contradicts the claim, explain why.
If there is no strong counter-evidence, you may still challenge logical leaps, missing context, or weak sources in the original claim.
If the claim seems solid, output disposition: REQUIRES_VERIFICATION.
You CANNOT output disposition: VERIFIED.
"""
        prompt = f"""
Original Claim: {claim.statement}
Original Evidence: {claim.evidence}
Original Sources: {', '.join(claim.source_urls)}

Counter-Evidence Search Results:
{results_context}

Produce a SkepticChallenge.
"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=SkepticChallenge
                )
            )
            
            if hasattr(response, 'parsed') and response.parsed:
                result: SkepticChallenge = response.parsed
            else:
                result = SkepticChallenge.model_validate_json(response.text)
                
            result.claim_id = claim.claim_id
            result.original_claim = claim.statement
            
            # -------------------------------------------------------------
            # EVIDENCE INTEGRITY VALIDATION
            # -------------------------------------------------------------
            val_res = EvidenceIntegrityValidator.validate_urls(result.counter_sources, retrieved_urls)
            result.counter_sources = val_res.accepted_urls
            
            if not val_res.valid:
                result.reasoning_summary += f" | WARNING: Removed hallucinated counter sources: {val_res.rejected_urls}"
            
            if result.disposition == "VERIFIED":
                result.disposition = "REQUIRES_VERIFICATION"
                result.reasoning_summary += " (Overridden: Skeptic cannot verify claims, only challenge them)"
                
            event_bus.publish(StreamingEvent(
                event_type=EventType.CHALLENGE_CREATED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="SkepticAgent",
                claim_id=claim.claim_id,
                payload={"type": result.challenge_type, "disposition": result.disposition}
            ))
            return result
        except ValidationError as ve:
            raise RuntimeError(f"Skeptic failed to validate challenge: {ve}")
        except Exception as e:
            raise RuntimeError(f"Skeptic failed to generate challenge: {e}")

    def _generate_adversarial_queries(self, claim: Claim) -> SearchQueryPlan:
        prompt = f"""
Generate 3 search queries specifically designed to find CONTRADICTORY evidence for this claim:
"{claim.statement}"
Think: What would someone search for if they wanted to prove this wrong?
"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SearchQueryPlan
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
            return SearchQueryPlan.model_validate_json(response.text)
        except:
            return SearchQueryPlan(queries=[f"evidence against {claim.statement}"])
