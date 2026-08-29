import os
import asyncio
import json
from app.agents.lead.agent import LeadAgent
from app.orchestration.research_orchestrator import ResearchOrchestrator

async def run_integration():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Please set GEMINI_API_KEY environment variable.")
        return
        
    lead = LeadAgent()
    orchestrator = ResearchOrchestrator()
    
    objective = "Find me a winning idea for this hackathon: https://devpost.com/software. I want to use Google GenAI APIs."
    constraints = ["Solo developer", "3 days to build"]
    
    print("--- 1. LEAD AGENT PLANNING ---")
    plan = lead.create_plan(objective, constraints)
    print(f"Plan generated with {len(plan.research_missions)} missions.")
    for m in plan.research_missions:
        print(f" - {m.specialist_role}: {m.objective}")
        
    print("\n--- 2. RESEARCH ORCHESTRATOR EXECUTING ---")
    batch = await orchestrator.execute_plan(plan, "inv_test_123", 1)
    
    print("\n--- 3. RESULTS ---")
    print(f"Findings: {len(batch.findings)}")
    print(f"Errors: {len(batch.errors)}")
    
    for f in batch.findings:
        print(f"\n[Role: {f.specialist_role}]")
        print(f"Summary: {f.summary}")
        print(f"Claims ({len(f.claims)}):")
        for c in f.claims:
            print(f"  - [{c.status}] {c.statement} (Source: {c.source})")
            
    print("\nFull JSON:")
    print(batch.model_dump_json(indent=2))

if __name__ == "__main__":
    asyncio.run(run_integration())
