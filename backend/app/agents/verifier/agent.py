import os
import asyncio
from typing import List, Optional, Set
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from app.models.research_finding import ResearchBatch, Claim
from app.models.lead_plan import LeadPlan
from app.models.skeptic_report import SkepticChallenge, SkepticReport
from app.models.verification_result import VerificationResult, EvidenceMatrixEntry
from app.services.research_tool import ResearchTool, DuckDuckGoSearchProvider
from app.agents.researchers.specialist import SearchQueryPlan

from app.models.events import StreamingEvent, EventType
from app.services.event_bus import event_bus
from app.services.evidence_integrity import EvidenceIntegrityValidator
from app.services.query_protector import DuplicateQueryProtector

class NormalizedClaim(BaseModel):
    normalized_proposition: str

class VerifierAgent:
    def __init__(self, api_key: str = None, model: str = None, search_provider: ResearchTool = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        self.search_provider = search_provider or DuckDuckGoSearchProvider()

    async def verify_batch(self, batch: ResearchBatch, skeptic_report: SkepticReport, plan: LeadPlan, executed_queries: Set[str] = None) -> List[VerificationResult]:
        event_bus.publish(StreamingEvent(
            event_type=EventType.VERIFIER_STARTED,
            investigation_id=batch.investigation_id,
            round_number=batch.research_round,
            agent="VerifierAgent"
        ))
        
        executed_queries = executed_queries if executed_queries is not None else set()
        
        # We only verify claims that were challenged by the Skeptic
        challenged_claim_ids = {chal.claim_id: chal for chal in skeptic_report.challenges}
        claims_to_verify = []
        for finding in batch.findings:
            for claim in finding.claims:
                if claim.claim_id in challenged_claim_ids:
                    claims_to_verify.append((claim, challenged_claim_ids[claim.claim_id]))
                    
        if not claims_to_verify:
            return []

        loop = asyncio.get_running_loop()
        tasks = []
        for claim, challenge in claims_to_verify:
            tasks.append(loop.run_in_executor(None, self._verify_single_claim, claim, challenge, plan, batch.investigation_id, batch.research_round, executed_queries))
            
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        verifications = []
        for r in results:
            if isinstance(r, Exception):
                print(f"Warning: Verifier failed on a claim: {r}")
            elif isinstance(r, VerificationResult):
                verifications.append(r)
                
        return verifications

    def _verify_single_claim(self, claim: Claim, challenge: SkepticChallenge, plan: LeadPlan, inv_id: str, round_num: int, executed_queries: Set[str]) -> VerificationResult:
        # Step 1: Normalize Claim
        normalized = self._normalize_claim(claim)
        
        # Step 2-4: Independent Search
        event_bus.publish(StreamingEvent(
            event_type=EventType.VERIFICATION_STARTED,
            investigation_id=inv_id,
            round_number=round_num,
            agent="VerifierAgent",
            claim_id=claim.claim_id
        ))
        
        queries = self._generate_verification_queries(normalized, claim, challenge)
        unique_queries, duplicate_queries = DuplicateQueryProtector.filter_queries(queries.queries, executed_queries)
        
        for dq in duplicate_queries:
            event_bus.publish(StreamingEvent(
                event_type=EventType.QUERY_DEDUPLICATED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="VerifierAgent",
                payload={"query": dq}
            ))
            
        search_results = []
        for query in unique_queries:
            try:
                search_results.extend(self.search_provider.search(query, max_results=3))
            except Exception as e:
                print(f"Verifier search failed for '{query}': {e}")
                
        retrieved_urls = [r.url for r in search_results]
                
        formatted_results = []
        for r in search_results:
            formatted_results.append(f"Title: {r.title}\nURL: {r.url}\nSnippet: {r.snippet}")
        results_context = "\n\n".join(formatted_results) if formatted_results else "No external search results found for independent verification."
        
        # Step 5 & 6: Adjudication
        system_instruction = """
You are the Verifier Agent for VERDICT. You are an independent evidence adjudicator.
You are NOT a summarizer, advocate, or another researcher producing an opinion.
Core Principle: "What does the evidence actually establish?"

Evaluate the Original Claim against the Skeptic's Challenge and your new Independent Search Results.
1. NEVER fabricate sources. Every external source MUST come from the search results provided.
2. VERIFIED must require actual evidence. Model knowledge alone can NEVER produce VERIFIED.
3. If reliable evidence directly contradicts the claim: REFUTED.
4. If only part of the claim is supported: PARTIALLY_VERIFIED.
5. If evidence conflicts substantially: CONTESTED.
6. If evidence is insufficient: INSUFFICIENT_EVIDENCE.
7. Return confidence between 0 and 1 representing confidence in your ADJUDICATION, not confidence that the claim is true.
"""
        prompt = f"""
Original Claim: {claim.statement}
Normalized Claim: {normalized.normalized_proposition}
Original Researcher Evidence: {claim.evidence}
Original Sources: {', '.join(claim.source_urls)}

Skeptic Challenge: {challenge.challenge_type} - {challenge.challenge_question}
Skeptic Counter-Evidence: {challenge.counter_evidence}
Skeptic Sources: {', '.join(challenge.counter_sources)}

### Independent Verification Search Results ###
{results_context}

Produce the final independent VerificationResult.
"""
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=VerificationResult
                )
            )
            
            if hasattr(response, 'parsed') and response.parsed:
                result: VerificationResult = response.parsed
            else:
                result = VerificationResult.model_validate_json(response.text)
                
            result.investigation_id = inv_id
            result.research_round = round_num
            result.claim_id = claim.claim_id
            result.original_claim = claim.statement
            result.normalized_claim = normalized.normalized_proposition
            
            # -------------------------------------------------------------
            # EVIDENCE INTEGRITY VALIDATION
            # -------------------------------------------------------------
            claimed_supporting = result.supporting_sources
            val_res = EvidenceIntegrityValidator.validate_urls(claimed_supporting, retrieved_urls)
            result.supporting_sources = val_res.accepted_urls
            
            valid_matrix = []
            for entry in result.evidence_matrix:
                entry_val = EvidenceIntegrityValidator.validate_urls([entry.source_url], retrieved_urls)
                if entry_val.valid and entry.source_url != "MODEL_KNOWLEDGE":
                    valid_matrix.append(entry)
                elif entry.source_url == "MODEL_KNOWLEDGE":
                    valid_matrix.append(entry)
                else:
                    event_bus.publish(StreamingEvent(
                        event_type=EventType.EVIDENCE_REJECTED,
                        investigation_id=inv_id,
                        round_number=round_num,
                        agent="VerifierAgent",
                        claim_id=claim.claim_id,
                        payload={"rejected_url": entry.source_url, "reason": "Hallucinated source"}
                    ))
            result.evidence_matrix = valid_matrix
            
            if not val_res.valid:
                result.verification_notes += f" | WARNING: Removed hallucinated supporting sources: {val_res.rejected_urls}"
            
            # Enforce evidence rules
            has_external_sources = len(result.supporting_sources) > 0 or len(result.evidence_matrix) > 0
            if result.verification_status == "VERIFIED" and not has_external_sources:
                result.verification_status = "INSUFFICIENT_EVIDENCE"
                result.verification_notes += " (Overridden: VERIFIED requires actual external evidence)"
                
            event_bus.publish(StreamingEvent(
                event_type=EventType.VERIFICATION_COMPLETED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="VerifierAgent",
                claim_id=claim.claim_id,
                payload={"status": result.verification_status}
            ))
            return result
            
        except ValidationError as ve:
            raise RuntimeError(f"Verifier failed to validate result output: {ve}")
        except Exception as e:
            raise RuntimeError(f"Verifier failed to generate result: {e}")

    def _normalize_claim(self, claim: Claim) -> NormalizedClaim:
        prompt = f"Rewrite the following claim into a precise testable proposition.\nClaim: {claim.statement}"
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=NormalizedClaim
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
            return NormalizedClaim.model_validate_json(response.text)
        except:
            return NormalizedClaim(normalized_proposition=claim.statement)

    def _generate_verification_queries(self, normalized: NormalizedClaim, claim: Claim, challenge: SkepticChallenge) -> SearchQueryPlan:
        prompt = f"""
Normalized Claim: {normalized.normalized_proposition}
Skeptic Challenge: {challenge.challenge_type} - {challenge.counter_evidence}

Generate 2 independent search queries to verify this dispute. 
Do not simply repeat the original query. Search for primary sources, official documentation, or credible reporting that resolves this specific dispute.
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
            return SearchQueryPlan(queries=[f"evidence regarding {normalized.normalized_proposition}"])
