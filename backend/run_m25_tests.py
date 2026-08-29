import os
import asyncio
from app.agents.lead.agent import LeadAgent
from app.orchestration.research_orchestrator import ResearchOrchestrator

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable to run live tests.")
        return
        
    lead = LeadAgent()
    orchestrator = ResearchOrchestrator()
    
    objective = "Find existing implementations of autonomous multi-agent research systems and determine whether this architecture is already common."
    constraints = []
    
    print("--- 1. LEAD AGENT PLANNING ---")
    plan = lead.create_plan(objective, constraints)
    print(f"Plan generated with {len(plan.research_missions)} missions.")
    
    print("\n--- 2. RESEARCH ORCHESTRATOR EXECUTING ---")
    batch = await orchestrator.execute_plan(plan, "inv_test_25", 1)
    
    print("\n--- 3. RESULTS ---")
    for f in batch.findings:
        print(f"\n[Role: {f.specialist_role}]")
        print(f"Summary: {f.summary}")
        print(f"Claims ({len(f.claims)}):")
        for c in f.claims:
            print(f"  - [{c.status}] {c.statement}")
            print(f"    Source Type: {c.source}")
            print(f"    Source URLs: {c.source_urls}")
            print(f"    Source Titles: {c.source_titles}")

if __name__ == "__main__":
    asyncio.run(run_integration())
