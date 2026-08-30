import os
import json
from typing import List, Set
from google import genai
from google.genai import types
from pydantic import BaseModel, ValidationError

from app.models.lead_plan import ResearchMissionPlan
from app.models.research_finding import ResearchFinding, Claim
from app.services.research_tool import ResearchTool, DuckDuckGoSearchProvider

from app.models.events import StreamingEvent, EventType
from app.services.event_bus import event_bus
from app.services.evidence_integrity import EvidenceIntegrityValidator
from app.services.query_protector import DuplicateQueryProtector

class SearchQueryPlan(BaseModel):
    queries: List[str]

class SearchQueryPlan(BaseModel):
    queries: List[str]

class SpecialistResearcher:
    def __init__(self, api_key: str = None, model: str = None, search_provider: ResearchTool = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set.")
        self.client = genai.Client(api_key=self.api_key)
        self.model = model or os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
        self.search_provider = search_provider or DuckDuckGoSearchProvider()

    def execute_mission(self, mission: ResearchMissionPlan, inv_id: str, round_num: int, executed_queries: Set[str] = None) -> ResearchFinding:
        event_bus.publish(StreamingEvent(
            event_type=EventType.RESEARCHER_STARTED,
            investigation_id=inv_id,
            round_number=round_num,
            agent="SpecialistResearcher",
            mission_id=mission.mission_id,
            payload={"role": mission.specialist_role}
        ))
        
        executed_queries = executed_queries if executed_queries is not None else set()
        
        # Step 1: Generate Queries
        queries = self._generate_search_queries(mission)
        
        unique_queries, duplicate_queries = DuplicateQueryProtector.filter_queries(queries.queries, executed_queries)
        for dq in duplicate_queries:
            event_bus.publish(StreamingEvent(
                event_type=EventType.QUERY_DEDUPLICATED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="SpecialistResearcher",
                payload={"query": dq}
            ))

        # Step 2: Execute Searches
        search_results = []
        for query in unique_queries:
            event_bus.publish(StreamingEvent(
                event_type=EventType.SEARCH_STARTED,
                investigation_id=inv_id,
                round_number=round_num,
                agent="SpecialistResearcher",
                mission_id=mission.mission_id,
                payload={"query": query}
            ))
            try:
                results = self.search_provider.search(query, max_results=3)
                search_results.extend(results)
                event_bus.publish(StreamingEvent(
                    event_type=EventType.SEARCH_COMPLETED,
                    investigation_id=inv_id,
                    round_number=round_num,
                    agent="SpecialistResearcher",
                    payload={"query": query, "results_count": len(results)}
                ))
            except Exception as e:
                print(f"Search failed for '{query}': {e}")
                
        retrieved_urls = [r.url for r in search_results]

        # Formatting context for the LLM
        formatted_results = []
        for r in search_results:
            formatted_results.append(f"Title: {r.title}\nURL: {r.url}\nSnippet: {r.snippet}")
            
        results_context = "\n\n".join(formatted_results) if formatted_results else "No external search results found."

        # Step 3: Synthesize Findings
        system_instruction = f"""
You are acting as a {mission.specialist_role}.
Your objective is: {mission.objective}
Review the provided Search Results and extract factual claims that address the specific questions.
1. NEVER fabricate source URLs. Every URL in source_urls MUST exactly match a URL from the Search Results.
2. If relying on your internal model knowledge for a claim, the source MUST be "MODEL_KNOWLEDGE" and source_urls MUST be empty.
3. claims should be highly specific and testable.
"""
        prompt = f"""
Mission Objective: {mission.objective}
Questions to answer: {mission.specific_questions}
Required Evidence: {mission.required_evidence}

### Search Results ###
{results_context}

Produce the final ResearchFinding.
"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=ResearchFinding
                )
            )
            
            if hasattr(response, 'parsed') and response.parsed:
                finding: ResearchFinding = response.parsed
            else:
                finding = ResearchFinding.model_validate_json(response.text)
                
            finding.mission_id = mission.mission_id
            finding.specialist_role = mission.specialist_role
            finding.research_round = round_num
            
            # -------------------------------------------------------------
            # EVIDENCE INTEGRITY VALIDATION
            # -------------------------------------------------------------
            for claim in finding.claims:
                claim.status = "UNVERIFIED"
                if "MODEL_KNOWLEDGE" not in claim.source_urls:
                    val_res = EvidenceIntegrityValidator.validate_urls(claim.source_urls, retrieved_urls)
                    claim.source_urls = val_res.accepted_urls
                    if not val_res.valid:
                        # Log rejected
                        event_bus.publish(StreamingEvent(
                            event_type=EventType.EVIDENCE_REJECTED,
                            investigation_id=inv_id,
                            round_number=round_num,
                            agent="SpecialistResearcher",
                            claim_id=claim.claim_id,
                            payload={"rejected_urls": val_res.rejected_urls}
                        ))
                    else:
                        event_bus.publish(StreamingEvent(
                            event_type=EventType.EVIDENCE_VALIDATED,
                            investigation_id=inv_id,
                            round_number=round_num,
                            agent="SpecialistResearcher",
                            claim_id=claim.claim_id,
                            payload={"accepted_urls": val_res.accepted_urls}
                        ))
                        
                event_bus.publish(StreamingEvent(
                    event_type=EventType.CLAIM_CREATED,
                    investigation_id=inv_id,
                    round_number=round_num,
                    agent="SpecialistResearcher",
                    claim_id=claim.claim_id,
                    payload={"statement": claim.statement}
                ))
                
            return finding
            
        except ValidationError as ve:
            raise RuntimeError(f"SpecialistResearcher failed to validate output: {ve}")
        except Exception as e:
            raise RuntimeError(f"SpecialistResearcher failed to generate finding: {e}")

    def _generate_search_queries(self, mission: ResearchMissionPlan) -> SearchQueryPlan:
        system_instruction = f"You are a {mission.specialist_role}. Generate exactly 3 highly targeted search queries to fulfill your mission."
        prompt = f"Objective: {mission.objective}\nQuestions: {mission.specific_questions}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=SearchQueryPlan
                )
            )
            if hasattr(response, 'parsed') and response.parsed:
                return response.parsed
            return SearchQueryPlan.model_validate_json(response.text)
        except Exception as e:
            # Fallback to a basic query if the model fails
            print(f"Warning: Failed to generate targeted queries, using fallback. Error: {e}")
            return SearchQueryPlan(queries=[mission.objective])
