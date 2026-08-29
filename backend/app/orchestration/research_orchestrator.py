import asyncio
from typing import List, Set
from app.models.lead_plan import LeadPlan, ResearchMissionPlan
from app.models.research_finding import ResearchFinding, ResearchBatch
from app.agents.researchers.specialist import SpecialistResearcher
from app.models.events import StreamingEvent, EventType
from app.services.event_bus import event_bus

class ResearchOrchestrator:
    def __init__(self, api_key: str = None):
        self.api_key = api_key
        self._researcher = SpecialistResearcher(api_key=self.api_key)

    async def _execute_single_mission(self, mission: ResearchMissionPlan, investigation_id: str, research_round: int, executed_queries: Set[str]) -> ResearchFinding:
        loop = asyncio.get_running_loop()
        try:
            finding = await loop.run_in_executor(
                None, 
                self._researcher.execute_mission, 
                mission, 
                investigation_id, 
                research_round,
                executed_queries
            )
            return finding
        except Exception as e:
            raise RuntimeError(f"Mission {mission.mission_id} failed: {e}")

    async def execute_plan(self, plan: LeadPlan, investigation_id: str, research_round: int = 1, executed_queries: Set[str] = None) -> ResearchBatch:
        executed_queries = executed_queries if executed_queries is not None else set()
        missions = plan.research_missions
        
        event_bus.publish(StreamingEvent(
            event_type=EventType.RESEARCH_PLAN_CREATED,
            investigation_id=investigation_id,
            round_number=research_round,
            payload={"mission_count": len(missions)}
        ))
        
        tasks = []
        for mission in missions:
            event_bus.publish(StreamingEvent(
                event_type=EventType.RESEARCH_MISSION_CREATED,
                investigation_id=investigation_id,
                round_number=research_round,
                mission_id=mission.mission_id,
                payload={"role": mission.specialist_role}
            ))
            tasks.append(self._execute_single_mission(mission, investigation_id, research_round, executed_queries))
            
        # Execute concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        findings = []
        errors = []
        
        for i, result in enumerate(results):
            mission_id = missions[i].mission_id
            if isinstance(result, Exception):
                print(f"[EVENT] RESEARCHER_FAILED: {mission_id} - {str(result)}")
                errors.append(str(result))
            else:
                print(f"[EVENT] RESEARCHER_COMPLETED: {mission_id}")
                for claim in result.claims:
                    print(f"[EVENT] CLAIM_CREATED: {claim.claim_id} ({claim.status})")
                findings.append(result)

        print("[EVENT] RESEARCH_BATCH_COMPLETED")
        
        return ResearchBatch(
            investigation_id=investigation_id,
            research_round=research_round,
            findings=findings,
            errors=errors
        )
